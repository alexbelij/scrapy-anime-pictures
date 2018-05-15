# scrapy-anime-pictures
 Crawl Image form https://anime-pictures.net use scrapy

### Induction

If you understand how scrapy work.

Just read Usage

### Installing

``` $ git clone git@github.com:urayoru113/scrapy-anime-pictures.git ```

### Prerequisites
``` $ pip install scrapy pillow ```


## Usage

### first

configure [**setting.ini**](/setting.ini) like:


```
[LOGIN]

account = asd12345
password = asd12345 


[IMG]
save_dir = ./Image 
minheight = 0 
minwidth = 0 
tags =
    love live
    naruto
    いとうのいぢ 
```
***
### note
1. If you don't understand how to configure. Just put what you want in tags

2. If you want to download R18 image, please set **account** and **password**

3. Use Romanization will avoid some error

4. Make sure your setting.ini encode in utf-8

### Running
``` $ scrapy crawl AnimePictures ```

# other
* Output file will sort by author, maybe I will let it can sort by tags(or by author) later
* I'm not sure whether cookie will execute correctly in browser

## version
  ver 1.0.0
