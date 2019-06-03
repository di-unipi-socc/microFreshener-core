from microfreshener.core.importer import YMLImporter
from microfreshener.core.analyser import MicroToscaAnalyserBuilder

import click

@click.command()
@click.argument('file', type=click.Path(exists=True))
def main(file):
    """
    MicroFreshener-core permits to analyse a microTosca (YML) file and to discover architectural smells
    """
    
    importer = YMLImporter()
    model = importer.Import(file)
    builder = MicroToscaAnalyserBuilder(model)
    analyser = builder.add_all_sniffers().build()
    res = analyser.run()
    print(res)

    
