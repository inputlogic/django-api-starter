# Django API Starter

## Installation

Save local environment variables:

```
mv env.template .env
```

Install requirements:

```
pip install -r requirements.init.txt
pip freeze > requirements.txt
rm requirements.init.txt
```

A note on `requirements.init.txt` vs `requirement.txt`:

> `requirement.init.txt` installs the latest versions of each package.
>
> If you have problems with the packages installed from `requirements.init.txt`,
> try installing django-api-starter's `requirements.txt` instead. It contains
> specific versions that are expected to work.
