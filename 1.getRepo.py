
# coding: utf-8

import ListProjects
import pandas as pd
import os
import time					  
import subprocess
import json
from github import Github

user_github = os.environ['usergit']
password_github = os.environ['pwdgit']



import os
if not os.path.exists('/gitgender/files/projects'):
    os.makedirs('/gitgender/files/projects')
	
clone_folder = '/tmp/clones/'
truckfactor_path_script = 'truckfactor/gittruckfactor/scripts/'
truckfactor_path_bin = 'truckfactor/gittruckfactor/target/'

lista_linguagens = [ 'javascript', 'python', 'java', 'ruby', 'php', 'cpp', 'css', 'csharp', 'go', 'c', 'typescript', 'shell', 'swift', 'scala', 'objective-c' ]
ListProjects.get_popular_projects(lista_linguagens)




df = pd.DataFrame(index=None,columns=None)

arquivos = os.listdir('/gitgender/files/projects')



def importFiles(folder):
    li = []
    for a in arquivos:
        print(a)
        df = pd.read_csv(folder + '/' + a, index_col=None, header=None)
        
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True, names=None, levels=None)
    return frame


def get_TruckFactor(repo_folder,full_name):
    global saida_jar
    p2 = subprocess.Popen(['./commit_log_script.sh', repo_folder + '/'], cwd=truckfactor_path_script)
    (out, err) = p2.communicate()
    if(err != None):
        print ("errors running commit_log_script : " + str(err))
    p3 = subprocess.Popen(['java', '-Xmx2G' ,'-Dlog4j.debug', '-Dlog4j.configuration=file:../bin/META-INF/log4j.xml', '-jar', 'gittruckfactor-1.0.jar', repo_folder, full_name], cwd=truckfactor_path_bin, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    

    (stdout, stderr) = p3.communicate()
    if(stderr != None):
        print ("errors running jar file : " + str(err))
    saida_jar = stdout
    commiters = []
    sp = False
    for o in saida_jar.decode().split("\n"):
        if (o.startswith('TF authors')):
            sp = True     
            continue
        if(sp and (o.rstrip() != "")):
            commiters.append(o)
    print("commiters saida get_TruckFactor: " + str(commiters))															   
    return commiters




def get_num_lines_repo(repo_folder):
    out = subprocess.Popen(['cloc', '--json', repo_folder], 
           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

								
    try:
        stdout,stderr = out.communicate()
        saida_cloc = json.loads(stdout.decode())	        
        total_lines = saida_cloc['SUM']['code']
    except:
        total_lines = '0'
    return total_lines

	
def getLoginfromCommit(name,repo):
    global df_commits
    print('nome: ' + name)
    df_commits_filtered = df_commits[df_commits[1]==name]
    #df_commits_filtered = df_commits_filtered[df_commits_filtered[4]==name]
    #print(df_commits_filtered)

    try:
        hash_commit=df_commits_filtered.tail(1)[0].values[0]
        commit = repo.get_commit(hash_commit)
        login = commit.author.login
    except:
        u = g.search_users(name)
        if (u.totalCount==1):
            login=u[0].login
        else:
            login=''
    return login

	
df_all = importFiles('/gitgender/files/projects')
df_commiters_ = pd.DataFrame(data=None,index=None,columns=None)
for line in df_all.iterrows():
    full_name = line[1][2]
    name = line[1][3]
    url = line[1][8]
    print('cloning {}...'.format(full_name))
    repo_folder = clone_folder + full_name.replace('/','_')
    p = subprocess.Popen(['git', 'clone', str(url), repo_folder ]) 
    
    (out, err) = p.communicate()
    if(err != None):
        print ("errors cloning repository: " + str(err))
    num_lines_repo = get_num_lines_repo(repo_folder)
    print('num_lines_repo' + str(num_lines_repo))
    
    
    commiters_tf = get_TruckFactor(repo_folder,full_name)
    
    linha = (*line[1], num_lines_repo)
    g = Github(user_github, password_github)
    repo = g.get_repo(full_name)
    new_file =  'commitinfo_d.log'
    f = open(repo_folder + '/commitinfo_d.log' , "w")
    p5 = subprocess.Popen(['iconv', '-c', '-f', 'utf8', '-t', 'utf8', repo_folder + '/' + 'commitinfo.log' ], cwd=repo_folder, stdout=f , stderr=subprocess.STDOUT)
    ret_code = p5.wait()    
    f.flush()
    (stdout, stderr) = p5.communicate()
    if(stderr != None):
        print ("errors changing encoding file : " + str(err))

    
    #os.system('iconv -c -f utf8 -t utf8 {} > {}'.format(repo_folder + '/' + 'commitinfo.log', '>', repo_folder + '/' +  'commitinfo_d.log'))
    df_commits = pd.read_csv(repo_folder + '/' + 'commitinfo_d.log',sep='-;-',header=None,index_col=None,encoding='utf-8')
    df_commits[1] = df_commits[1].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    df_commits.drop_duplicates(subset=[1,4],inplace=True)
    print('num of TF found:' + str(len(commiters_tf)))
    for n in commiters_tf:
        print('name of commiter: ' + n)
        n = n.split(sep=';')
        n = n[0]
        login = getLoginfromCommit(n,repo)
        #tp_commiters_tf = tuple(n)
        #print(tp_commiters_tf)
        tp_commiters_tf = n + ';' + login
        tp_commiters_tf = tp_commiters_tf.split(sep=';')
        #tp_commiters_tf = tuple(n + ';' + login)
        linha2 = (linha + tuple(tp_commiters_tf))
        print(linha2)            
        linha3 = pd.Series(linha2,index=None)

        df_commiters_ = df_commiters_.append(linha3,ignore_index=True)
    p = subprocess.Popen(['rm', '-rf', repo_folder ]) 


df_commits.to_csv('df_commits.csv',header=False,index=False,index_label=False)
df_commiters_.to_csv('commiters_with_TF3.csv',header=False,index=False,index_label=False)




