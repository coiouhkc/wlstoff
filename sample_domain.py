import os
import wlstoff as wo

domainName = 'sample'

wo.start(os.environ['WL_HOME'] + '/common/templates/wls/wls.jar')
wo.createDomain(domainName)
wo.createMachine('')
wo.createAdminServer('adminserver', '', 8001, '')
wo.configureServerLogging(domainName, 'adminserver')
wo.configureMaxRequestParameter('adminserver', -1)
wo.createWlsAdminUser('wlsadmin', 'wlsadmin1')
wo.createDatasource('ds1', 'jdbc/ds1', 'oracle.jdbc.driver.OracleDriver', 'jdbc:oracle:thin:@(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = host1)(PORT = 1521)) (ADDRESS = (PROTOCOL = TCP)(HOST = host2)(PORT = 1521)) (CONNECT_DATA =  (SERVER = DEDICATED) (SERVICE_NAME = service1)))', 'ds1username', 'ds1password', 'SQL SELECT 1 FROM DUAL', 'adminserver')
wo.createDatasource('ds2', 'jdbc/ds2', 'com.ibm.db2.jcc.DB2Driver', 'jdbc:db2://myhost:50001/mydb', 'ds2username', 'ds2password', 'SQL SELECT 1 FROM SYSIBM.SYSTABLES', 'adminserver')

wo.createMailSession('mail/MailSession', 'mail/MailSession', 'mail.from=noreply@mydomain;mail.transport.protocol=smtp;mail.host=mymail', 'adminserver')

wo.createJms('MyJmsServer', 'MyJmsModule', 'MyConnectionFactory', 'jms/QCF', ['Mdb1', 'Mdb2'], ['jms/MyQueue1', 'jms/MyQueue2'], 'MyJmsSubModule', 'adminserver')

wo.createSecurity('adminserver', '/opt/SP/scripts/identity.jks', 'identitysecret', '/opt/SP/scripts/trust.jks', 'trustsecret', 'mykey', 'mykeysecret')

wo.fixBasicAuth(domainName)

wo.finish('/var/SP/weblogic/' + domainName)
