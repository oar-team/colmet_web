# Flask web interface to graph colmet data using Matplotlib/Mpld3
# Configure:
#     Setup the path to colmet HDF5 file right after this comments
# Launching:
#     python colmet_web.py
# Using:
#     Point a browser to http://localhost:5000
#

APIURI="http://localhost/oarapi"
APILIMIT="1000"
cluster_name="Froggy"
CACHING=True
CACHING_JOBS_FILE="/scratch/chandler.jobs.cache"
CACHING_JOBS_DELAY=120


####################################################################
from flask import Flask
app = Flask(__name__)
from flask import request,render_template,url_for,abort,redirect,make_response
import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import mpld3
import json
import zlib
import requests
import sys,os,time,re
from distutils.version import StrictVersion as version

matplotlib.use('Agg')


# Functions
def get_from_api(uri):
    """
        Get an object from the api
    """
    headers = {'Accept': 'application/json'}
    r = requests.get(APIURI+uri+"?limit="+APILIMIT,headers=headers)
    if r.status_code != 200:
        print ("Could not get "+APIURI+uri)
        r.raise_for_status()
    if version(requests.__version__) >= version("2.0.0"):
        return r.json()
    else:
        return r.json

def get(uri,cache_file,cache_delay):
    """
        Get from the cache or from the api
    """
    if CACHING and os.path.isfile(cache_file) and time.time() - os.path.getmtime(cache_file) < cache_delay:
        json_data=open(cache_file)
        return json.load(json_data)
    else:
        data=get_from_api(uri)
    if CACHING:
        chmod=True
        if os.path.isfile(cache_file):
            chmod=False
        file=open(cache_file,'w')
        json.dump(data,file)
        file.close
        if chmod:
            os.chmod(cache_file, 0666)
    return data

def get_jobs():
    """
        Get the current jobs list from the OAR API
    """
    return get('/jobs/details',CACHING_JOBS_FILE,CACHING_JOBS_DELAY)["items"]

def get_job_metrics(id,raw=0):
    """
        Get colmet metrics for a given job
    """
    headers = {'Accept': 'application/x-gzip'}
    r = requests.get(APIURI+"/colmet/job/"+str(id),headers=headers)
    if r.status_code != 200:
        print ("Could not get colmet data for job "+str(id))
        r.raise_for_status()
    if raw==1:
      return r.content
    else:
      return json.loads(zlib.decompress(r.content,zlib.MAX_WBITS|32))


def compute_cumul(data):
    """
        Compute cumulative time dependent data
        Take a time:data dictionnary as input and return an array of data/time_unit values
    """
    init=1
    out_data=[]
    v_prev=0
    value=0
    for t in sorted(data):
        y=data[t]
        if init==0:
            value=(y-y_prev)/(t-t_prev)
            # In case it wraps around to 0, keep the old value
            if value < 0:
                value = v_prev
            out_data.append(value)
        else:
            init=0
            out_data.append(0)
        y_prev=y
        t_prev=t
        v_prev=value
    return out_data

def reduce(data,size,mode):
    """
        Reduces a list to a floating average if mode=0, or the middle value if mode=1
        The size parameter is the final length of the list
    """
    chunk_size=int(len(data)/size)
    if mode == 0:
      convol_list=[ 1.0/chunk_size for i in range(0,chunk_size) ]
    else:
      convol_list=[ 0 for i in range(0,chunk_size/2) ]
      convol_list.append(1)
      convol_list.extend([ 0 for i in range(chunk_size/2,chunk_size-1) ])
    return np.convolve(data,convol_list,mode='valid')[::chunk_size]  
 
# Routes

@app.route('/')
def index():
    jobs=get_jobs()
    jobs=[ j for j in jobs if j["state"]=="Running" ]
    return render_template('index.html',cluster_name=cluster_name,jobs=jobs,now=int(time.time()))

@app.route('/form/job')
def form_job():
    id=request.args.get('id', '')
    begin=request.args.get('begin', '')
    end=request.args.get('end', '')
    return render_template('form_job.html',cluster_name=cluster_name,def_id=id,def_begin=begin,def_end=end,def_res=500)

# Cpu/mem/io graphs
@app.route('/graph/job')
def graph_job():
    # Read parameters
    id=int(request.args.get('id', '0'))
    t_min=request.args.get('t_min', '0')
    if t_min == '':
        t_min=0
    else:
        t_min=int(t_min)
    t_max=request.args.get('t_max', '7200')
    if t_max=='':
       t_max=7200
    else:
       t_max=int(t_max)
    total_points=int(request.args.get('resolution', '500'))
    type=request.args.get('type', 'graph')

    # Return raw data (extract only)
    if type == "extract":
        metrics=get_job_metrics(id,1)
        response = make_response()
        response.headers['Content-type']='application/json' 
        response.headers['Content-Encoding']='gzip'
        response.headers['Content-Disposition']='attachment; filename="'+str(id)+'.json"'
        response.data=metrics
        return response

    # Prepare graphs
    fig={}
    graph={}
    for g in [ 'cpu','mem','read','write']:
        fig[g] = plt.figure(figsize=(9,5))
        graph[g] = fig[g].add_subplot(111)

    # Load the metrics
    # TODO: reemplacer cette lecture directe du fichier hdf5 par une extraction de l'api OAR
    #f = h5py.File(colmetfile, "r")
    #metrics=f['job_'+str(id)+'/metrics']['timestamp','hostname','ac_etime','cpu_run_real_total','coremem','read_bytes','write_bytes']
    #f.close
    ##############################################

    metrics=get_job_metrics(id)

    # Set the origin timestamp
    origin=metrics['timestamp'][0]
    # Get a list of uniq hosts
    hosts = set(metrics['hostname'])
    # For each host
    for host in hosts:
      # Prepare host and timestamp filter
      def filter(idx):
        return metrics['hostname'][idx] == host and t_min < metrics['timestamp'][idx]-origin < t_max
      # X axis is a number of seconds starting at 0
      x=[ a for idx,a in enumerate(metrics['timestamp']) if filter(idx) ]
      x0=x[0]
      x=[ (a - x0) for a in x ]
      x=reduce(x,total_points,1)
      # Cpu
      y_cpu=[ 1.0*a/metrics['ac_etime'][idx]/1000 for idx,a in enumerate(metrics['cpu_run_real_total']) if filter(idx) ]
      y_cpu=reduce(y_cpu,total_points,0)
      graph['cpu'].plot(x,y_cpu,label=host,lw=5,alpha=0.4)
      # Memory
      y_mem={ metrics['ac_etime'][idx]: 1.0*a/1024 for idx,a in enumerate(metrics['coremem']) if filter(idx) }
      y_mem=compute_cumul(y_mem)
      y_mem=reduce(y_mem,total_points,0)
      graph['mem'].plot(x,y_mem,label=host,lw=5,alpha=0.4)
      graph['mem'].set_ylabel('rss (GBytes)')
      # Read/Write
      y_read={ metrics['timestamp'][idx]: 1.0*a/1024/1024 for idx,a in enumerate(metrics['read_bytes']) if filter(idx) }
      y_read=compute_cumul(y_read)
      y_read=reduce(y_read,total_points,0)
      graph['read'].plot(x,y_read,label=host,lw=5,alpha=0.4)
      graph['read'].set_ylabel('Read (MBytes/s)')
      y_write={ metrics['timestamp'][idx]: 1.0*a/1024/1024 for idx,a in enumerate(metrics['write_bytes']) if filter(idx) }
      y_write=compute_cumul(y_write)
      y_write=reduce(y_write,total_points,0)
      graph['write'].plot(x,y_write,label=host,lw=5,alpha=0.4)
      graph['write'].set_ylabel('Write (MBytes/s)')
    # Print a legend and generate html
    html={}
    for g in [ 'cpu','mem','read','write']:
        graph[g].legend()
        graph[g].grid(color='lightgray', alpha=0.7)
        graph[g].set_xlabel('time (s)')
        html[g]=mpld3.fig_to_html(fig[g])
    # Rendering 
    plt.close("all")
    return render_template('show_job_graphs.html', graph=html)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
