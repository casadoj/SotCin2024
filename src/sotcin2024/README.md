To download data from the Early Warning Data Store (EWDS), you need to install first the API of the Climate Data Store (CDS):

```pip install "cdsapi>=0.7.4"```

or

```conda install conda-forge::cdsapi```

You also need a [CDS account](https://cds.climate.copernicus.eu/). Once you have an account and you're logged in, this [link](https://ewds.climate.copernicus.eu/how-to-api) will show you two lines of code like these:

```url: https://ewds.climate.copernicus.eu/api
key: xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx```

Copy those two lines and create a file named _.cdsapirc_:

* If you're using **Linux**, the file must be saved in _$HOME/.cdsapirc_.
* If you're using **Windows**, the file must be saved in _C:\Users\<USERNAME>\.cdsapirc_.
