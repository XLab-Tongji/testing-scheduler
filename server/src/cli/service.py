#!/usr/bin/env python
import click
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SERVICE_DIR = os.path.join(BASE_DIR, "..", "env", "service")

@click.command()
@click.option("--filepath", help="filepath of the service .yaml file.")
def registerService(filepath):
  if os.path.exists(filepath):
    with open(filepath, "r") as f:
      content = f.read()
    (fileDir, serviceName) = os.path.split(filepath)
    serviceFilePath = os.path.join(SERVICE_DIR, serviceName) 
    with open(serviceFilePath, "w") as f:
      f.write(content)
  else:
    print "No such file!"

if __name__ == "__main__":
	registerService()