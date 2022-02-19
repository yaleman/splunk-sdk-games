#!/bin/bash


echo "Generating local JSON 'export' data"
time python ./write_raw_json.py

echo "Generating local JSON 'create' data"
time python ./write_raw_json_job_create.py

echo ""
echo "Generating local XML data"
time python write_raw_xml.py

echo ""
echo "File sizes"
echo ""
ls -lah outputfile*

echo ""
echo "Running test_file_jsonreader.py"
time python test_file_jsonreader.py

echo ""
echo "Running test_file_jsonreader_create.py"
time python test_file_jsonreader_create.py

echo ""
echo "Running test_file_resultsreader.py"
time python test_file_resultsreader.py

echo ""
echo "Done!"
