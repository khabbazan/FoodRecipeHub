# Food Recipe Hub Translation

This README provides guidance on implementing and managing translation within the application.

## Introduction

In Food Recipe Hub, translation is facilitated through the use of the `InternationalizationMiddleware` middleware and the `make_gettext` function in the [FastAPI BABEL](https://pypi.org/project/fastapi-babel/) module. The initial instance and primary configuration can be found in the `src/core/babel` directory.

## Translation Files

Translation files are stored in the `locale/` directory, coming in two formats: `.mo` and `.po`. The `.po` files are used for updating and maintaining translations, while the `.mo` files are compiled versions used for runtime translation.

### Updating `.po` Files

To update the `.po` files, follow these steps:

1. Create a `babel.cfg` file with the following content:
   ```ini
   [python: **.py]

2. Generate a .pot (Portable Object Template) file from your source code:
   ```bash
   pybabel extract -F babel.cfg -o locale/messages.pot src/
   ```

3. Update the `.pot` file with the existing `.po` file for your desired language (replace `<LANGUAGE>` with the appropriate language code):
   ```bash
   pybabel update -i locale/messages.pot -d locale -l <LANGUAGE>
   ```
   Ensure to replace `<LANGUAGE>` with the language code you are working with.


### Generating `.mo` Files
After updating the `.po` files, generate the corresponding `.mo` files for runtime use with this command:

   ```bash
   pybabel compile -d locale
   ```
### Installing the FastAPI BABEL Package

To ensure you have the [FastAPI BABEL](https://pypi.org/project/fastapi-babel/) package installed in your environment, follow these instructions:

   ```bash
   pip install fastapi-babel==0.0.8
   ```
