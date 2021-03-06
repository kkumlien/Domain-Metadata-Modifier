'''
Created on Sep 26, 2017

@author: stevepark
'''
import unittest
import os
from unittest.mock import MagicMock, PropertyMock
from metadata.FileFinder import FileFinder
from metadata.Common import Common

class FileFinderTest(unittest.TestCase):
    
    common = Common()
    
    DOMAIN_SCHEMA_FILE = """<?xml version="1.0" encoding="UTF-8"?>
<semanticLayerDataSource>
    <folder></folder>
    <name>Domain_Test</name>
    <schema>
        <localResource
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            exportedWithPermissions="false" dataFile="schema.data" xsi:type="fileResource">
            <folder></folder>
        </localResource>
    </schema>
</semanticLayerDataSource>
    """
    ADHOC_TOPIC_FILE = """<?xml version="1.0" encoding="UTF-8"?>
<dataDefinerUnit>
    <folder></folder>
    <name>Adhoc_Topic_Test</name>
    <mainReport>
        <localResource
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            exportedWithPermissions="false" dataFile="slJRXML.data" xsi:type="fileResource">
            <folder></folder>
        </localResource>
    </mainReport>
    <dataSource>
        <uri>/Domain_Test</uri>
    </dataSource>
    <resource>
        <localResource
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            exportedWithPermissions="false"
            dataFile="domainQuery.xml.data" xsi:type="fileResource">
            <folder></folder>
        </localResource>
    </resource>
</dataDefinerUnit>
    """
    ADHOC_VIEW_FILE = """<?xml version="1.0" encoding="UTF-8"?>
<adhocDataView exportedWithPermissions="true">
    <folder></folder>
    <name>Adhoc_View_Test</name>
    <dataSource>
        <uri>/Adhoc_Topic_Test</uri>
    </dataSource>
    <inputControl>
        <localResource
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            exportedWithPermissions="false" xsi:type="inputControl">
            <folder>/Adhoc_View_Test_files</folder>
            <name>store_country_1</name>
            <label>Country</label>
            <type>4</type>
            <mandatory>false</mandatory>
            <readOnly>false</readOnly>
            <visible>true</visible>
            <query>
                <localResource exportedWithPermissions="false" xsi:type="query">
                    <folder>/Adhoc_View_Test_files/store_country_1_files</folder>
                    <name>store_country_1</name>
                    <version>0</version>
                    <label>Country</label>
                    <language>domain</language>
                    <queryString>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;query xmlns="http://www.jaspersoft.com/2007/SL/XMLSchema"&gt;
  &lt;groupList&gt;
    &lt;group columnName="store_country" /&gt;
  &lt;/groupList&gt;
  &lt;queryFields&gt;
    &lt;queryField id="public_store.store_country" /&gt;
    &lt;queryField id="store_country" /&gt;
  &lt;/queryFields&gt;
&lt;/query&gt;
                        </queryString>
                    <dataSource>
                        <uri>/Domain_Test</uri>
                    </dataSource>
                </localResource>
            </query>
            <queryVisibleColumn>store_country</queryVisibleColumn>
            <queryValueColumn>store_country</queryValueColumn>
        </localResource>
    </inputControl>
    <resource>
        <uri>/domainQuery.xml</uri>
    </resource>
    <resource>
        <localResource
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            exportedWithPermissions="false" dataFile="topicJRXML.data" xsi:type="fileResource">
            <folder></folder>
            <name>topicJRXML</name>
        </localResource>
    </resource>
    <resource>
        <localResource
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            exportedWithPermissions="false" dataFile="stateXML.data" xsi:type="fileResource">
            <folder></folder>
            <name>stateXML</name>
        </localResource>
    </resource>
</adhocDataView>
    """
    REPORT_FILE = """<?xml version="1.0" encoding="UTF-8"?>
<reportUnit exportedWithPermissions="true">
    <folder></folder>
    <name>Report_Test</name>
    <mainReport>
        <localResource
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            exportedWithPermissions="false"
            dataFile="mainReportJrxml.data" xsi:type="fileResource">
            <folder></folder>
            <name>mainReportJrxml</name>
        </localResource>
    </mainReport>
    <dataSource>
        <uri>/Adhoc_View_Test</uri>
    </dataSource>
    <resource>
        <localResource
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            exportedWithPermissions="false" dataFile="stateXML.data" xsi:type="fileResource">
            <folder></folder>
            <name>stateXML</name>
        </localResource>
    </resource>
</reportUnit>
    """
    XML_EXT = '.xml'
    DOMAIN_NAME = 'Domain_Test'
    ADHOC_TOPIC_NAME = 'Adhoc_Topic_Test'
    ADHOC_VIEW_NAME = 'Adhoc_View_Test'
    REPORT_NAME = 'Report_Test'
    TMPPATH = 'tmp'

    def setUp(self):
        self.fileFinder = FileFinder()
        self.log = self.common.configureLogging()
        curr_folder = Common.REPO_PATH_SEPARATOR + self.TMPPATH
        self.fileFinder.resources_folder = curr_folder
        self.domain_metadata_file_path = curr_folder + Common.REPO_PATH_SEPARATOR + self.DOMAIN_NAME + self.XML_EXT
        self.adhoc_topic_metadata_file_path = curr_folder + Common.REPO_PATH_SEPARATOR + self.ADHOC_TOPIC_NAME + self.XML_EXT
        self.adhoc_view_metadata_file_path = curr_folder + Common.REPO_PATH_SEPARATOR + self.ADHOC_VIEW_NAME + self.XML_EXT
        self.report_metadata_file_path = curr_folder + Common.REPO_PATH_SEPARATOR + self.REPORT_NAME + self.XML_EXT
        directory = os.path.dirname(self.domain_metadata_file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(self.domain_metadata_file_path, 'w') as h1:
            h1.write(self.DOMAIN_SCHEMA_FILE)
        with open(self.adhoc_topic_metadata_file_path, 'w') as h2:
            h2.write(self.ADHOC_TOPIC_FILE)
        with open(self.adhoc_view_metadata_file_path, 'w') as h3:
            h3.write(self.ADHOC_VIEW_FILE)
        with open(self.report_metadata_file_path, 'w') as h4:
            h4.write(self.REPORT_FILE)

    def tearDown(self):
        try:
            os.remove(self.report_metadata_file_path)
            os.remove(self.adhoc_view_metadata_file_path)
            os.remove(self.adhoc_topic_metadata_file_path)
            os.remove(self.domain_metadata_file_path)
        except OSError:
            pass
        
    def testCheckDatasource(self):
        mock_root = MagicMock(name = 'mock_root')
        mock_root.tag.find.return_value = 0
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = 0
        mock_root.__getitem__.return_value = mock_node1
        self.assertTrue(self.fileFinder.checkDatasource(mock_root))
        
    def testCheckDatasourceDoesNotMatch(self):
        mock_root = MagicMock(name = 'mock_root')
        mock_root.tag.find.return_value = 0
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = -1
        mock_root.__getitem__.return_value = mock_node1
        self.assertFalse(self.fileFinder.checkDatasource(mock_root))
        
    def testCheckDatasourceCheckParent(self):
        self.fileFinder.domain_id = self.DOMAIN_NAME
        mock_root = MagicMock(name = 'mock_root');
        mock_root.tag.find.side_effect = [-1, 0]
        mock_node1 = MagicMock(name='mock_node1')
        mock_node1_text = PropertyMock(return_value=Common.REPO_PATH_SEPARATOR + self.DOMAIN_NAME)
        type(mock_node1).text = mock_node1_text
        node_list = [mock_node1]
        mock_root.xpath = MagicMock(side_effect=[node_list])
        self.assertTrue(self.fileFinder.checkDatasource(mock_root))

    def testFindDomainSchema(self):
        schema_filename = 'schema.data'
        self.fileFinder.domain_id = self.DOMAIN_NAME
        mock_grandchild = MagicMock(name='mock_grandchild')
        mock_grandchild_text = PropertyMock(return_value='')
        type(mock_grandchild).text = mock_grandchild_text
        mock_root = MagicMock(name = 'mock_root')
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.get.return_value = schema_filename
        mock_node1.__getitem__.return_value = mock_grandchild
        node_list = [mock_node1]
        mock_root.xpath = MagicMock(side_effect=[node_list])
        found_file = self.fileFinder.findDomainSchema(root=mock_root, log=self.log)
        self.assertIsNotNone(found_file, 'findDomainSchemaFile should not return none')
        self.assertEqual(Common.REPO_PATH_SEPARATOR + self.TMPPATH + Common.REPO_PATH_SEPARATOR + schema_filename, found_file, 'domain schema file not found')
            
    def testFindDomainSchemaFile(self):
        found_file = self.fileFinder.findDomainSchemaFile(metadata_filename=self.domain_metadata_file_path, log=self.log)
        self.assertIsNotNone(found_file, 'findDomainSchema should not return none')
        test_domain_schema_file = '/tmp/schema.data'
        self.assertEqual(test_domain_schema_file, found_file, 'domain schema file names do not match')
    
    def testFindAdHocTopic(self):
        state_file = 'stateXML.data'
        jrxml_file = 'slJRXML.data'
        self.fileFinder.domain_id = self.DOMAIN_NAME
        self.fileFinder.adhoc_topic_files_list = []
        mock_grandchild = MagicMock(name='mock_grandchild')
        mock_grandchild_text = PropertyMock(return_value=self.DOMAIN_NAME)
        type(mock_grandchild).text = mock_grandchild_text
        mock_grandchild.text = MagicMock(return_value=self.DOMAIN_NAME)
        mock_grandchild2 = MagicMock(name='mock_grandchild2')
        mock_grandchild2_text = PropertyMock(return_value=None)
        type(mock_grandchild2).text = mock_grandchild2_text 
        mock_root = MagicMock(name = 'mock_root')
        mock_root_tag = PropertyMock(return_value=Common.DOMAIN_METADATA_TAG)
        type(mock_root).tag = mock_root_tag
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = 0
        mock_node2 = MagicMock(name = 'mock_node2')
        mock_node2.__getitem__.return_value = mock_grandchild2
        mock_node2.get.return_value = jrxml_file
        mock_node2.text.find.return_value = 0
        node_list1 = [mock_node2]
        mock_node3 = MagicMock(name = 'mock_node3')
        mock_node3.__getitem__.return_value = mock_grandchild2
        mock_node3.get.return_value = state_file
        node_list2 = [mock_node3]
        mock_node4 = MagicMock(name='mock_node4')
        mock_node4_text = PropertyMock(return_value=self.ADHOC_TOPIC_NAME)
        type(mock_node4).text = mock_node4_text
        mock_root.__getitem__.side_effect = [mock_node1, mock_grandchild]
        mock_root.xpath = MagicMock(side_effect = [node_list1, node_list2])
        self.fileFinder.findAdhocTopic(root=mock_root, adhoc_topic_id=self.ADHOC_TOPIC_NAME, log=self.log)
        self.assertNotEqual([], self.fileFinder.adhoc_topic_files_list, 'Ad Hoc topic files not found')
        self.assertEqual(Common.REPO_PATH_SEPARATOR + self.TMPPATH + Common.REPO_PATH_SEPARATOR + state_file, self.fileFinder.adhoc_topic_files_list[0][0], 'state file not found')
        self.assertEqual(Common.REPO_PATH_SEPARATOR + self.TMPPATH + Common.REPO_PATH_SEPARATOR +  jrxml_file, self.fileFinder.adhoc_topic_files_list[0][1], 'jrxml file not found')
        
    def testFindAdHocTopicIDDoesNotMatch(self):
        self.fileFinder.adhoc_topic_files_list = []
        mock_root = MagicMock(name = 'mock_root')
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = -1
        mock_root.__getitem__.return_value = mock_node1
        self.fileFinder.findAdhocTopic(root=mock_root, adhoc_topic_id=self.ADHOC_TOPIC_NAME, log=self.log)
        self.assertEqual([], self.fileFinder.adhoc_topic_files_list, 'ad hoc topic files should not be found')
            
    def testFindAdHocTopicFiles(self):
        self.fileFinder.adhoc_topic_files_list = []
        self.fileFinder.domain_id = self.DOMAIN_NAME
        self.fileFinder.findAdhocTopicFiles(metadata_filename=self.adhoc_topic_metadata_file_path, adhoc_topic_id=self.ADHOC_TOPIC_NAME, log=self.log)
        self.assertNotEqual([], self.fileFinder.adhoc_topic_files_list, 'Ad Hoc topic files list is empty')
        test_adhoc_topic_state_file = '/tmp/domainQuery.xml.data'
        self.assertEqual(test_adhoc_topic_state_file, self.fileFinder.adhoc_topic_files_list[0][0], 'ad hoc topic state file names do not match')
        test_adhoc_topic_report_file = '/tmp/slJRXML.data'
        self.assertEqual(test_adhoc_topic_report_file, self.fileFinder.adhoc_topic_files_list[0][1], 'jrxml report file names do not match')
        
    def testFindAdHocTopicFilesIDDoesNotMatch(self):
        self.fileFinder.adhoc_topic_files_list = []
        self.fileFinder.domain_id = self.DOMAIN_NAME
        self.fileFinder.findAdhocTopicFiles(metadata_filename=self.adhoc_topic_metadata_file_path, adhoc_topic_id='Some_Other_Topic', log=self.log)
        self.assertEqual([], self.fileFinder.adhoc_topic_files_list, 'Ad Hoc topic files should not be found')
        
    def testFindAdHocView(self):
        state_filename = 'stateXML.data'
        jrxml_filename = 'topicJRXML.data'
        self.fileFinder.adhoc_view_files_list = []
        self.fileFinder.domain_id = self.DOMAIN_NAME
        mock_grandchild = MagicMock(name='mock_grandchild')
        mock_grandchild_text = PropertyMock(return_value='')
        type(mock_grandchild).text = mock_grandchild_text
        mock_root = MagicMock(name = 'mock_root')
        mock_root.tag.find.return_value = 0
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = 0
        mock_node1.get.return_value = state_filename
        mock_node2 = MagicMock(name = 'mock_node2')
        mock_node2.get.return_value = jrxml_filename
        mock_node3 = MagicMock(name = 'mock_node3')
        mock_node3_text = PropertyMock(return_value=state_filename)
        type(mock_node3).text = mock_node3_text
        mock_node4 = MagicMock(name = 'mock_node4')
        mock_node4_text = PropertyMock(return_value=jrxml_filename)
        type(mock_node4).text = mock_node4_text
        mock_node1.__getitem__.side_effect = [mock_node3, mock_grandchild]
        mock_node2.__getitem__.side_effect = [mock_node4, mock_grandchild]
        node_list = [mock_node1, mock_node2]
        mock_root.__getitem__.side_effect = [mock_node1, mock_node1]
        mock_root.xpath = MagicMock(side_effect = [node_list, []])
        self.fileFinder.findAdhocView(root=mock_root, adhoc_view_id=self.ADHOC_VIEW_NAME, log=self.log)
        self.assertNotEqual([], self.fileFinder.adhoc_view_files_list, 'Ad Hoc view files not found')
        self.assertEqual(Common.REPO_PATH_SEPARATOR + self.TMPPATH + Common.REPO_PATH_SEPARATOR + state_filename, self.fileFinder.adhoc_view_files_list[0][0], 'state file not found')
        self.assertEqual(Common.REPO_PATH_SEPARATOR + self.TMPPATH + Common.REPO_PATH_SEPARATOR +  jrxml_filename, self.fileFinder.adhoc_view_files_list[0][1], 'jrxml file not found')
    
    def testFindAdHocViewIDDoesNotMatch(self):
        mock_root = MagicMock(name = 'mock_root')
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = -1
        mock_root.__getitem__.return_value = mock_node1
        self.fileFinder.findAdhocView(root=mock_root, adhoc_view_id=self.ADHOC_VIEW_NAME, log=self.log)
        self.assertEqual([], self.fileFinder.adhoc_view_files_list, 'ad hoc view files should not have been found')
            
    def testFindAdHocViewFiles(self):
        self.fileFinder.domain_id = self.DOMAIN_NAME
        self.fileFinder.adhoc_view_files_list = []
        self.fileFinder.findAdhocViewFiles(metadata_filename=self.adhoc_view_metadata_file_path, adhoc_view_id=self.ADHOC_VIEW_NAME, log=self.log)
        self.assertNotEqual([], self.fileFinder.adhoc_view_files_list, 'Ad Hoc view files not found')
        test_adhoc_view_state_file = '/tmp/stateXML.data'
        self.assertEqual(test_adhoc_view_state_file, self.fileFinder.adhoc_view_files_list[0][0], 'ad hoc view state file names do not match')
        test_adhoc_view_report_file = '/tmp/topicJRXML.data'
        self.assertEqual(test_adhoc_view_report_file, self.fileFinder.adhoc_view_files_list[0][1], 'jrxml report file names do not match')
        
    def testFindAdHocViewFilesIDDoesNotMatch(self):
        self.fileFinder.findAdhocViewFiles(metadata_filename=self.adhoc_view_metadata_file_path, adhoc_view_id='Some_Other_View', log=self.log)
        self.assertEqual([], self.fileFinder.adhoc_view_files_list, 'Ad Hoc view files should not be found')
        
    def testFindReport(self):
        state_filename = 'stateXML.data'
        jrxml_filename = 'mainReportJrxml.data'
        self.fileFinder.report_list = []
        mock_grandchild = MagicMock(name='mock_grandchild')
        mock_grandchild_text = PropertyMock(return_value=self.TMPPATH)
        type(mock_grandchild).text = mock_grandchild_text
        mock_grandchild2 = MagicMock(name='mock_grandchild2')
        mock_grandchild2_text = PropertyMock(return_value=None)
        type(mock_grandchild2).text = mock_grandchild2_text
        mock_root = MagicMock(name = 'mock_root')
        mock_root.tag.find.return_value = 0
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = 0
        mock_node2 = MagicMock(name = 'mock_node2')
        mock_node2.text.find.return_value = 0
        mock_node2.get.return_value = state_filename
        mock_node2.__getitem__.return_value = mock_grandchild2
        node_list1 = [mock_node2]
        mock_node3 = MagicMock(name = 'mock_node3')
        mock_node3.get.return_value = jrxml_filename
        mock_node3.__getitem__.return_value = mock_grandchild2
        mock_root.__getitem__.return_value = mock_node1
        node_list2 = [mock_node3]
        mock_root.xpath = MagicMock(side_effect = [node_list2, node_list1])
        self.fileFinder.findReport(root=mock_root, report_id=self.REPORT_NAME, log=self.log)
        self.assertNotEqual([], self.fileFinder.report_list, 'Report files not found')
        self.assertEqual(Common.REPO_PATH_SEPARATOR + self.TMPPATH + Common.REPO_PATH_SEPARATOR + state_filename, self.fileFinder.report_list[0][0], 'state filenames do not match')
        self.assertEqual(Common.REPO_PATH_SEPARATOR + self.TMPPATH + Common.REPO_PATH_SEPARATOR + jrxml_filename, self.fileFinder.report_list[0][1], 'report filenames do not match')
        
    def testFindStaticReport(self):
        jrxml_filename = 'main_jrxml.data'
        self.fileFinder.report_list = []
        mock_grandchild = MagicMock(name='mock_grandchild')
        mock_grandchild.text = MagicMock(return_value=self.TMPPATH)
        mock_grandchild2 = MagicMock(name='mock_grandchild2')
        mock_grandchild2_text = PropertyMock(return_value=None)
        type(mock_grandchild2).text = mock_grandchild2_text
        mock_root = MagicMock(name = 'mock_root')
        mock_root.tag.find.return_value = 0
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = 0
        mock_node2 = MagicMock(name = 'mock_node3')
        mock_node2.get.return_value = jrxml_filename
        mock_node2.__getitem__.return_value = mock_grandchild2
        mock_root.__getitem__.return_value = mock_node1
        node_list1 = [mock_node2]
        mock_root.xpath = MagicMock(side_effect = [node_list1, []])
        self.fileFinder.findReport(root=mock_root, report_id=self.REPORT_NAME, log=self.log)
        self.assertNotEqual([], self.fileFinder.report_list, 'Report files not found')
        self.assertIsNone(self.fileFinder.report_list[0][0], 'state filename is not None')
        self.assertEqual(Common.REPO_PATH_SEPARATOR + self.TMPPATH + Common.REPO_PATH_SEPARATOR + jrxml_filename, self.fileFinder.report_list[0][1], 'jrxml filenames do not match')
        
    def testFindReportIDDoesNotMatch(self):
        self.fileFinder.adhoc_view_files_list = []
        self.fileFinder.report_list = []
        mock_root = MagicMock(name = 'mock_root')
        mock_node1 = MagicMock(name = 'mock_node1')
        mock_node1.text.find.return_value = -1
        mock_root.__getitem__.return_value = mock_node1
        self.fileFinder.findReport(root=mock_root, report_id=self.REPORT_NAME, log=self.log)
        self.assertEqual([], self.fileFinder.report_list, 'report files should not have been found')
            
    def testFindReportFiles(self):
        self.fileFinder.domain_id = self.DOMAIN_NAME
        self.fileFinder.findReportFiles(metadata_filename=self.report_metadata_file_path, report_id=self.REPORT_NAME, log=self.log)
        self.assertNotEqual([], self.fileFinder.report_list, 'report files not found')
        test_report_state_file = '/tmp/stateXML.data'
        self.assertEqual(test_report_state_file, self.fileFinder.report_list[0][0], 'report state file names do not match')
        test_report_jrxml_file = '/tmp/mainReportJrxml.data'
        self.assertEqual(test_report_jrxml_file, self.fileFinder.report_list[0][1], 'jrxml report file names do not match')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()