# test-quickSign
> This repositery contains reponse to question present in files README-Subject.md
### Project structure
pyton source is in folder `src/core`

My answers are divided to 2 files

- Answer to point 1 to 4 is in python file `upload_image.py`
- Answer to point 5 to 6 is in python file `api_image.py`

Mongo colllections structures are defined in file `image_table.py`

You need to have at least python.3.6 installed 

#### To load images in mongo database 
```bash
python src/core/upload_image.py
```

#### To launch Flask api servces
```bash
python src/core/api_image.py.py
```