#!/bin/bash


echo "Generating local JSON data"
time python ./write_raw_json.py

echo ""
echo "Generating local XML data"
time python write_raw_xml.py

echo ""
echo "File sizes"
echo ""
ls -lah outputfile.*

echo ""
echo "Running test_file_jsonreader.py"
time python test_file_jsonreader.py

echo ""
echo "Running test_file_resultsreader.py"
time python test_file_resultsreader.py

echo ""
echo "Done!"
