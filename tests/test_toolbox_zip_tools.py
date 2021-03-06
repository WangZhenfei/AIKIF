import unittest
import sys
import os
import time
import aikif.config as mod_cfg
import aikif.lib.cls_filelist as fl 

root_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." ) 
sys.path.append(root_folder + os.sep + 'aikif' + os.sep + 'toolbox' )
import zip_tools

#src_file = os.getcwd() + os.sep + 'data.txt'
src_file = 'data.txt'
with open(src_file, 'w') as f:
    f.write('this is some unzipped text')

op_folder      = os.getcwd()
test_file2     = os.getcwd() + os.sep + 'test2.zip'
test_file2     = 'test2.zip'  # relative path
nested_zipfile = os.getcwd() + os.sep + 'test_nested.zip'

folder_to_zip = root_folder + os.sep + 'aikif' + os.sep + 'data'

class ToolboxZipToolsTest(unittest.TestCase):
    def test_01_create_zip_from_file(self):
        zip_tools.create_zip_from_file(test_file2, src_file)
        lst1 = fl.FileList([os.getcwd()], ['test2.zip'], [],  '')
        self.assertEqual('test2.zip' in lst1.get_list()[0], True ) 


    def test_02_create_zip_from_folder(self):
        zip_tools.create_zip_from_folder(nested_zipfile, folder_to_zip )
        lst1 = fl.FileList([os.getcwd()], ['*.zip'], [],  '')
        #print(lst1.get_list())
        self.assertEqual(len(lst1.get_list()) > 1, True) 
        #self.assertEqual(lst1.get_list()[0], 'T:\\user\\dev\\src\\python\\AIKIF\\tests\\test_results\\test_nested.zip') 
        
    def test_03_extract_all(self):
        os.remove(src_file) # no try needed - you create this file at the start of the test
        self.assertEqual(os.path.exists(src_file), False)  # make sure orig file is gone 
        zip_tools.extract_all(test_file2, op_folder) # os.getcwd()
        time.sleep(1)
        self.assertEqual(os.path.exists(src_file), True)  # Wow - the file is back!
        
        
    def test_10_instantiate_class(self):
        z = zip_tools.ZipFile(test_file2)
        #print(z.type)
        self.assertEqual(z.type,'ZIP')

    def test_11_extract(self):
        z = zip_tools.ZipFile(test_file2)
        z.extract(op_folder)
        
        lst1 = fl.FileList([op_folder], ['*.*'], [],  '')
        #print(lst1.get_list())
        self.assertEqual(len(lst1.get_list()) > 1, True) 
        extract_fldr = op_folder + os.sep

    def test_20_type_GZ(self):
        zip_tools.create_gz_from_content('test.gz', b"some data for GZ file")
        zip_tools.extract_all('test.gz', op_folder)
        self.assertEqual(os.path.exists('test.gz'), True)

    def test_21_type_TAR(self):
        zip_tools.create_tar_from_files('test.tar', ['test.gz', 'test2.zip'])
        self.assertEqual(os.path.exists('test.tar'), True)
        time.sleep(1)
        os.remove('test.gz') 
        os.remove('test2.zip') 
        self.assertEqual(os.path.exists('test.gz'), False)
        self.assertEqual(os.path.exists('test2.zip'), False)
        zip_tools.extract_all('test.tar', op_folder )
        self.assertEqual(os.path.exists('test.gz'), True)
        self.assertEqual(os.path.exists('test2.zip'), True)
                
 
if __name__ == '__main__':
    unittest.main()
