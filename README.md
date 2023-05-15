# 🌌 APOD Wallpaper Picker

### 🔭 About

> **Environment:** Visual Studio 1.78.2 (user setup) | **Python 3.10.9** (conda).

This script allows the user to **get and set the APOD (Astronomy Picture of the Day) wallpaper** using the NASA API. 
In addition, metadata with detailed information about the image are downloaded from the response, which are also printed. 
At the first start-up, a configuration file is generated, which must be supplemented with user data. It looks like this:

```json
{
    "api_key": "",
    "default_wallpaper": "",
    "style": ""
}
```

- ```"api_key"``` - User can generate **NASA API key** here: https://api.nasa.gov/
- ```"default_wallpaper"``` means **the path to the default wallpaper file** (it will be set when something goes wrong).
- ```"style"``` - **The style of the wallpaper display** (`fill`, `fit`, `stretch`, `tile`, `center`, `span`).

