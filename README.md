pythonwebmap
============

To add this project to your OpenShift application it is probably best to merge it locally on your machine and then push it to your OpenShift application. You can trying with --from-code but I think the size of the JSON file is too large

After creating your application (in this case I am assuming you named your application pythonwebmap) on your local machine, do the following commands:

  cd pythonwebmap
  git remote add upstream -m master https://github.com/thesteve0/pythonwebmap.git
  git pull -s recursive -X theirs upstream master
  git push
  




The data come from the GNIS at the USGS and is in the public domain.
http://gnis.usgs.gov/domestic/download_data.htm
Concise Features – Large features that should be labeled on maps with a scale of 1:250,000. Subset of National file above.
(last updated October 2, 2009) 
