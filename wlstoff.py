import os
import sys
import socket

sys.path.append(os.environ['WL_HOME'] + '/common/wlst/modules')

import wlstModule as wlst

def start(templatePathName):
	wlst.WLS.setShowLSResult(0)
	print ("Reading template: " + templatePathName)
	wlst.readTemplate(templatePathName)
	print ("Done.")
	
def finish(domainPathName):
	print ("Finishing")
	wlst.setOption('OverwriteDomain', 'true')
	print ("	Writing Domain")
	wlst.writeDomain(domainPathName)
	print ("	Done")
	print ("	Closing template")
	wlst.closeTemplate()
	print ("	Done")
	print ("Done")

def createDomain(domainName):
	print ("Creating domain: " + domainName)
	print ("Done")

def createMachine(machineAddress, nodeManagerAddress=None, nodeManagerPort=0, nodeManagerType=None):
	if not machineAddress:
		machineAddress = socket.gethostbyname(socket.gethostname())
	print ("Creating machine")
	wlst.cd('/')
	wlst.create(machineAddress, 'UnixMachine')
	wlst.cd('/Machines/' + machineAddress)
	wlst.set('PostBindGID', 'nobody')
	wlst.set('PostBindGIDEnabled', 'false')
	wlst.set('PostBindUID', 'nobody')
	wlst.set('PostBindUIDEnabled', 'false')

	wlst.create(machineAddress, 'NodeManager')
	wlst.cd('NodeManager/' + machineAddress)
	wlst.set('Name', machineAddress)

	if (not nodeManagerType is None):
		wlst.cd('Machines/' + machineAddress + '/NodeManager/' + machineAddress)
		wlst.set('NMType', nodeManagerType)
		wlst.set('ListenPort', nodeManagerPort)
		configureNodeManagerProperties(nodeManagerPort)

	print("Done")

def createCluster(clusterName):
	print ("Creating cluster")
	wlst.cd('/')
	wlst.create(clusterName, 'Cluster')
	print ("Done")

def createServer(serverName, serverAddress, serverPort, serverMachine, serverArguments):
	if not serverAddress:
		serverAddress = socket.gethostbyname(socket.gethostname())
	if not serverMachine:
		serverMachine = socket.gethostbyname(socket.gethostname())
	wlst.cd('/Server/' + serverName)
	wlst.set('Name', serverName)
	wlst.set('ListenAddress', serverAddress)
	wlst.set('ListenPort', serverPort)
	wlst.set('Machine', serverMachine)

	if serverArguments:
		configureServerStart(serverName, serverArguments)

def configureServerStart(serverName, serverArguments):
	wlst.cd('/Server/' + serverName)
	wlst.create(serverName, 'ServerStart')
	wlst.cd('ServerStart/' + serverName)
	wlst.set('Arguments', serverArguments)

def createAdminServer(serverName, serverAddress, serverPort, serverMachine, serverArguments=None):
	print ("Creating admin server")
	createServer(serverName, serverAddress, serverPort, serverMachine, serverArguments)
	print ("Done")

def createManagedServer(serverName, serverAddress, serverPort, serverMachine, cluster, serverArguments=None):
	print ("Creating managed server")
	wlst.cd('/')
	wlst.create(serverName, 'Server')
	createServer(serverName, serverAddress, serverPort, serverMachine, serverArguments)
	wlst.cd('/Server/' + serverName)
	wlst.set('ClientCertProxyEnabled', 'true')
	wlst.set('WeblogicPluginEnabled', 'true')
	if cluster:
		wlst.assign('Server', serverName, 'Cluster', cluster)
	print ("Done")

def configureServerLogging(domainName, serverName, domainLogRoot='/var/SP/applogs/weblogic'):
	print ("Configuring server logging")

	wlst.cd('/')
	wlst.create(domainName + 'Log', 'Log')
	wlst.cd('Log/' + domainName + 'Log')
	wlst.set('Filename', domainLogRoot + '/' + domainName + '/domain/' + domainName + '.log')
	wlst.set('RotationType', 'byTime')

	wlst.cd('/Server/' + serverName)
	wlst.create(serverName, 'Log')
	wlst.cd('Log/' + serverName)
	wlst.set('RotationType', 'byTime')
	wlst.set('FileCount', 1)
	wlst.set('FileName', domainLogRoot + '/' + domainName + '/' + serverName + '/' + serverName + '.log')
	wlst.set('MemoryBufferSeverity', 'Debug')
	wlst.set('NumberOfFilesLimited', 'false')
	wlst.set('RedirectStderrToServerLogEnabled', 'true')
	wlst.set('RedirectStdoutToServerLogEnabled', 'true')
	wlst.set('RotateLogOnStartup', 'false')
	wlst.set('RotationTime', '23:59')

#	wlst.set('DateFormatPattern', 'dd.MM.yyyy HH:mm:ss')
#	wlst.set('FileMinSize', 100000)
#	wlst.set('LogFileSeverity', 'Debug')
#	wlst.set('StdoutSeverity', 'Debug')
#	wlst.set('StacktraceDepth', -1)
#	wlst.set('DomainLogBroadcastSeverity', 'Debug')
#	wlst.set('MemoryBufferSeverity', 'Debug')
#	wlst.set('RedirectStdoutToServerLogEnabled', 'true')
#	wlst.set('RedirectStderrToServerLogEnabled', 'true')

	wlst.cd('/Server/' + serverName)
	wlst.create(serverName, 'WebServer')
	wlst.cd('WebServer/' + serverName)
	wlst.create(serverName, 'WebServerLog')
	wlst.cd('WebServerLog/' + serverName)
	wlst.set('RotationType', 'byTime')
	wlst.set('FileCount', 1)
	wlst.set('FileName', domainLogRoot + '/' + domainName + '/' + serverName + '/access.log')
	wlst.set('FileTimeSpan', 1)
	wlst.set('LogFileRotationDir', domainLogRoot + '/' + domainName + '/' + serverName + '/archive')
	wlst.set('NumberOfFilesLimited', 'false')
	wlst.set('RotateLogOnStartup', 'false')
	print ("Done")
	
def configureMaxRequestParameter(serverName, maxRequestParameter):
	print ("Configuring MaxRequestParameter")
	wlst.cd('/Server/' + serverName)
	wlst.create(serverName, 'WebServer')
	wlst.cd('WebServer/' + serverName)
	
	wlst.set('MaxRequestParameterCount', maxRequestParameter)
	print ("Done")
	
def createWlsAdminUser(username, password):
	print ("Creating admin user")
	wlst.cd('/Security/base_domain/User')
	wlst.delete('weblogic', 'User')
	wlst.create(username, 'User')
	wlst.cd(username)
	wlst.set('Password', password)
	wlst.set('IsDefaultAdmin', '1')
	wlst.assign('User', username, 'Group', 'Deployers')
	print ("Done")

def createDatasource(dsName, dsJndiName, driver, url, username, password, test, target):
	print ("Creating data source: " + dsName)
	wlst.cd('/')
	wlst.create(dsName, 'JDBCSystemResource')
	wlst.cd('JDBCSystemResource/' + dsName + '/JdbcResource/' + dsName)
	
	wlst.create(dsName + 'DataSourceParams', 'JDBCDataSourceParams')
	wlst.cd('JDBCDataSourceParams/NO_NAME_0')
	wlst.set('JNDIName', dsJndiName)
	wlst.set('GlobalTransactionsProtocol', 'EmulateTwoPhaseCommit')
	
	wlst.cd('/JDBCSystemResource/' + dsName + '/JdbcResource/' + dsName)
	wlst.create(dsName + 'JDBCDriverParams', 'JDBCDriverParams')
	wlst.cd('JDBCDriverParams/NO_NAME_0')
	wlst.set('DriverName', driver)
	wlst.set('URL', url)
	wlst.set('PasswordEncrypted', password)
	wlst.create('myProps', 'Properties')

	wlst.cd('Properties/NO_NAME_0')
	wlst.create('user', 'Property')
	wlst.cd('Property/user')
	wlst.set('Value', username)
	
	wlst.cd('/JDBCSystemResource/' + dsName + '/JdbcResource/' + dsName)
	wlst.create(dsName + 'PoolParams', 'JDBCConnectionPoolParams')
	wlst.cd('JDBCConnectionPoolParams/NO_NAME_0')
	wlst.set('TestTableName', test)
	wlst.set('CapacityIncrement', 1)
	wlst.set('InitialCapacity', 0)
	wlst.set('MinCapacity', 0)
	wlst.set('MaxCapacity', 20)
	wlst.set('LoginDelaySeconds', 0)
	wlst.set('TestConnectionsOnReserve', 'true')
	wlst.set('FatalErrorCodes', '-4470,-4498,-4499,-99999')
	
	wlst.cd('/')
	wlst.assign('JDBCSystemResource', dsName, 'Target', target)

	print ("Done")
	
def createMailSession(msName, msJndiName, properties, target):
	print ("Creating mail session")
	wlst.cd('/')
	wlst.create(msName, 'MailSession')
	wlst.cd('/MailSession/(' + msName + ')')
	wlst.set('JNDIName', msJndiName)
	wlst.set('Properties', properties)
	wlst.assign('MailSession', msName, 'Target', target)
	print ("Done")

def createJms(jmsServerName, jmsModuleName, cfName, cfJndiName, queueNames, queueJndiNames, jmsSubName, target):
	print ("Creating Jms")
	wlst.cd ('/')
	if (wlst.ls().find('JMSServer') == -1 or wlst.ls('JMSServer').find(jmsServerName) == -1):
		wlst.create(jmsServerName, 'JMSServer')
	
	wlst.cd ('/')
	if (wlst.ls().find('JMSSystemResource') == -1 or wlst.ls('JMSSystemResource').find(jmsModuleName) == -1):
		wlst.create(jmsModuleName, 'JMSSystemResource')
		
	wlst.cd('/JMSSystemResource/' + jmsModuleName)
	if (wlst.ls().find('SubDeployment') == -1 or wlst.ls('SubDeployment').find(jmsSubName) == -1):
		wlst.create(jmsSubName, 'SubDeployment')
	
	wlst.cd('/')
	wlst.assign('JMSServer', jmsServerName, 'Target', target)
	wlst.assign('JMSSystemResource', jmsModuleName, 'Target', target)
	wlst.assign('JMSSystemResource.SubDeployment', jmsSubName, 'Target', jmsServerName)
	
	wlst.cd('/JMSSystemResource/' + jmsModuleName + '/JmsResource/NO_NAME_0')
	wlst.create(cfName, 'ConnectionFactory')
	wlst.cd ('ConnectionFactory/' + cfName)
	wlst.set('JNDIName', cfJndiName)
	wlst.set('SubDeploymentName', jmsSubName)
	
	for i in range(len(queueNames)):
		queueName = queueNames[i]
		queueJndiName = queueJndiNames[i]
		wlst.cd('/JMSSystemResource/' + jmsModuleName + '/JmsResource/NO_NAME_0')
		wlst.create(queueName, 'Queue')
		wlst.cd('Queue/' + queueName)
		wlst.set('JNDIName', queueJndiName)
		wlst.set('SubDeploymentName', jmsSubName)
		
	print ("Done")

def fixJms(jmsServerName, jmsModuleName, cfName, cfJndiName, queueNames, queueJndiNames, jmsSubName, target):
	wlst.cd('/')
	wlst.unassign('JMSSystemResource.SubDeployment', jmsSubName, 'Target', target)
	wlst.unassign('JMSSystemResource.SubDeployment', jmsSubName, 'Target', jmsServerName)
	wlst.assign('JMSSystemResource.SubDeployment', jmsSubName, 'Target', jmsServerName)
	
def createSecurity(serverName, identityFileName, identityPassword, trustFileName, trustPassword, keyAlias, keyPassword):
	print ("Creating Security (Keystores)")
	wlst.cd('/')
	wlst.cd('Server/' + serverName)
	
	wlst.set('KeyStores', 'CustomIdentityAndCustomTrust')
	wlst.set('CustomIdentityKeyStoreFileName', identityFileName)
	wlst.set('CustomIdentityKeyStorePassPhraseEncrypted', identityPassword)
	wlst.set('CustomIdentityKeyStoreType', 'JKS')
	
	wlst.set('CustomTrustKeyStoreFileName', trustFileName)
	wlst.set('CustomTrustKeyStorePassPhraseEncrypted', trustPassword)
	wlst.set('CustomTrustKeyStoreType', 'JKS')
	
	wlst.create(serverName, 'SSL')
	wlst.cd('SSL/' + serverName)
	wlst.set('ServerPrivateKeyAlias', keyAlias)
	wlst.set('ServerPrivateKeyPassPhraseEncrypted', keyPassword)
	wlst.set('ClientCertAlias', keyAlias)
	wlst.set('ClientCertPrivateKeyPassPhraseEncrypted', keyPassword)
	
	wlst.set('UseClientCertForOutbound', 'true')
	wlst.set('UseServerCerts', 'true')
	print ("Done")
	
def configureCompleteWriteTimeout(serverName, timeout):
	print ("Creating CompleteWriteTimeout")
	wlst.cd('/')
	wlst.cd('Server/' + serverName)
	wlst.set('CompleteWriteTimeout', timeout)
	print ("Done")

def configureDevelopmentJTATransactionTimeout(serverName, timeout):
	print 'Setting JTS timeout'
	wlst.cd('/')
	wlst.create('JTA', 'JTA')
	wlst.cd('/JTA/JTA')
	wlst.set('TimeoutSeconds', timeout)
	print ("Done")

def configureWebServer(serverName):
	print ("Configuring webserver parameters")
	wlst.cd('/Server/' + serverName)
	wlst.cd('WebServer/' + serverName)
	wlst.set('KeepAliveSecs', 5)
	wlst.set('MaxRequestParameterCount', 125000)
	wlst.set('MaxRequestParamterCount', 125000)
	print ("Done")

def configureNodeManagerProperties(nmPort):
	print ("Configuring NodeManager")
	wlst.cd('/')
	wlst.cd('NMProperties')
	wlst.set('ListenPort', nmPort)
	wlst.set('SecureListener', 'false')
	print ("Done")

def fixBasicAuth(domainName):
	print ("Fixing BasicAuth intercept")
	if (wlst.ls().find('SecurityConfiguration') == -1 or wlst.ls('SecurityConfiguration').find(domainName) == -1):
		wlst.create(domainName, 'SecurityConfiguration')
	wlst.cd('/SecurityConfiguration/' + domainName)
	wlst.set('EnforceValidBasicAuthCredentials', 'false')
	print ("Done")


