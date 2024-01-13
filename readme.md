# :sunrise: retime :city_sunset:

> Time your GNOME Dynamic Wallpapers to be synchronise with your local
> sunrise and sunset times using the [Open-Meteo API](https://open-meteo.com/en/docs/).

## Installation

0. Install

   ```
   pip install -r requirements.txt
   sudo make install
   ```

1. [Configure](#configuration)

## Configuration

Configuration happens in two files: `$XDG_CONFIG_HOME/.config/retime/config.toml` and
`retime.toml` located inside the folder with the images.

### `config.toml`

Contains your location data and options to modify the durutions of certain times.
An example is shown below and in [`config.toml`](./config.toml).

```toml
latitude = 51.5007343
longitude = -0.1257605

sunrise-sunset-factor = 1 # multiply duration of sunrise and sunset (default: 1)
transition-duration = 5 # seconds (default: 5)
```

### `retime.toml`

This goes at the root of the directory containing the images to use for the wallpaper.
An example is shown below.

```toml
# the images over which sunrise happens
sunrise = [ "Lakeside-3.jpg", "Lakeside-4.jpg", "Lakeside-5.jpg" ]
# the images over which the day passes
day = [ "Lakeside-6.jpg", "Lakeside-7.jpg", "Lakeside-8.jpg" ]
# the images over which sunset happens
sunset = [ "Lakeside-9.jpg", "Lakeside-10.jpg", "Lakeside-11.jpg" ]
# the images over which the night passes
night = [ "Lakeside-12.jpg", "Lakeside-1.jpg", "Lakeside-2.jpg" ]
```
