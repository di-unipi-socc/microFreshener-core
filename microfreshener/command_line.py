import os
import click
import json

from microfreshener.core.importer import JSONImporter, YMLImporter
from microfreshener.core.exporter import JSONExporter, YMLExporter
from microfreshener.core.analyser import MicroToscaAnalyserBuilder

@click.group()
def cli():
    """
    MicroFreshener permits to analyse microservice based architectures to discover architectural smells.
    """
    

@cli.command()
@click.argument('ymlfile', type=click.Path(exists=True))
def analyse(ymlfile):
    """
    Analyse a microTOSCA YML
    """
    importer = YMLImporter()
    model = importer.Import(ymlfile)
    builder = MicroToscaAnalyserBuilder(model)
    analyser = builder.add_all_sniffers().build()
    res = analyser.run()
    click.echo(res)

    
@cli.command()
@click.argument('ymlfile', type=click.Path(exists=True))
@click.argument('jsonfile')
def ymltojson(ymlfile, jsonfile):
    """
    Transform a microTOSCA YML file to JSON
    """

    yml_importer = YMLImporter()
    json_exporter = JSONExporter()
    mmodel = yml_importer.Import(ymlfile)
    jsonString = json_exporter.Export(mmodel)
    with open(jsonfile, 'w') as outfile:
        json.dump(jsonString, outfile, indent=4)


@cli.command()
@click.argument('jsonfile',type=click.Path(exists=True))
@click.argument('ymlfile')
def jsontoyml(jsonfile, ymlfile):
    """
    Transform a JSON file into microTosca YML file
    """

    model = JSONImporter().Import(jsonfile)
    ymlString = YMLExporter().Export(model)
    click.echo(ymlString)
    with open(ymlfile, 'w') as outfile:
        outfile.write(ymlString) 