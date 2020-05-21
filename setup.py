from distutils.core import setup

setup(name='bgpvis',
      version='0.1',
      description='BGP visualisation/analysis',
      author='Hynek Los',
      author_email='hynek.los@gmail.com',
      url='https://github.com/hynek2001/bgpvis',
      packages=['PyBGPdump', 'pandas','plotly'],
     )