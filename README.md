# Victus RGB (Linux)

Control the keyboard RGB lighting on **HP Victus laptops** directly from Linux by writing RGB values to the Embedded Controller (EC).

This project was created after reverse-engineering how the lighting values are stored in EC memory. It allows you to change keyboard colors and run lighting effects without Windows or OMEN Gaming Hub.

there's a [Rust version](https://github.com/najisheheem05/victus-tuner) of this project with more features and uses fewer resources, I would recommend that over this 

---

## Features

- Change keyboard RGB color directly from Linux
- No Windows or proprietary software required
- Simple command line interface
- Lightweight (single Python script)
- Automatic EC access setup
- Background lighting effects
- Automatic replacement of running effects

Supported lighting modes:

- Static colors
- Custom RGB
- Rainbow
- Breathing effect
- Alternate between two colors
- Fade between two colors

---

## How It Works

The keyboard lighting values are stored in EC registers.

The RGB values are written starting at **offset `0x08`** inside EC memory.

Example values discovered during testing:

| Color | EC Bytes   |
| ----- | ---------- |
| Red   | `e4 00 00` |
| Green | `00 e4 00` |
| Blue  | `00 00 e4` |

The program writes RGB values directly to:

```

/sys/kernel/debug/ec/ec0/io

```

---

## Requirements

- Linux
- Root access
- `ec_sys` kernel module

The program automatically loads the module when needed.

---

## Installation

### Option 1: Download the precompiled binary (recommended)

No Python installation required — this is a standalone binary.

Download the latest release:

```bash
sudo curl -L https://github.com/hseyinblgc/RGB_Tuner4Victus/releases/latest/download/victus-rgb -o /usr/local/bin/victus-rgb
sudo chmod +x /usr/local/bin/victus-rgb
```

Then run commands like:

```bash
sudo victus-rgb color red
```

### Option 2: Run from source

Requires Python 3.

Clone the repository:

```bash
git clone https://github.com/hseyinblgc/RGB_Tuner4Victus.git
cd RGB_Tuner4Victus
```

Run directly with Python:

```bash
sudo python victus-rgb.py color red
```

---

## Preset Colors

| Color       | Command                       |
| ----------- | ----------------------------- |
| red         | `sudo victus-rgb color red`         |
| green       | `sudo victus-rgb color green`       |
| blue        | `sudo victus-rgb color blue`        |
| yellow      | `sudo victus-rgb color yellow`      |
| cyan        | `sudo victus-rgb color cyan`        |
| purple      | `sudo victus-rgb color purple`      |
| neon-purple | `sudo victus-rgb color neon-purple` |
| white       | `sudo victus-rgb color white`       |
| off         | `sudo victus-rgb color off`         |
| fire        | `sudo victus-rgb color fire`        |
| flame       | `sudo victus-rgb color flame`       |

Example:

```bash
sudo victus-rgb color neon-purple
```

---

## Custom RGB

You can set any RGB color.

```
sudo victus-rgb color R G B
```

Example:

```bash
sudo victus-rgb color 120 40 255
```

---

## Read Current Color

Display the RGB value currently stored in the EC.

```bash
sudo victus-rgb current
```

Example output:

```
Current RGB: 255 0 0
```

---

## Lighting Effects

All lighting effects run **in the background** and continue even after the terminal closes.

Starting a new effect **automatically stops the previous one**.

---

### Rainbow

Cycle through all colors smoothly.

```bash
sudo victus-rgb rainbow
```

Adjust speed:

```bash
sudo victus-rgb --speed 8 rainbow
```

---

### Breathing Effect

Fade brightness in and out.

```bash
sudo victus-rgb breathe red
```

Adjust speed:

```bash
sudo victus-rgb --speed 7 breathe neon-purple
```

---

### Alternate Between Two Colors

Switch between two colors repeatedly.

```bash
sudo victus-rgb alternate red blue
```

Adjust speed:

```bash
sudo victus-rgb --speed 8 alternate red blue
```

---

### Fade Between Two Colors

Smooth transition between two colors.

```bash
sudo victus-rgb fade red blue
```

Adjust speed:

```bash
sudo victus-rgb --speed 8 fade neon-purple cyan
```

---

All of these effects can be run using RGB values as well ("R G B R G B" if there are 2 colors : else R G B)

```bash
sudo victus-rgb fade 255 0 0 0 255 0
```

---

## Stop Effects

Stop all running lighting effects.

```bash
sudo victus-rgb stop
```

---

## Supported Hardware

Tested on:

- HP Victus 16

Other Victus and Omen models may work if they use the same EC RGB layout.

---

## Warning

This tool writes directly to EC registers.

Incorrect values may:

- freeze the keyboard controller
- crash the EC
- require a hard reboot

Use at your own risk.

## License

MIT Licence