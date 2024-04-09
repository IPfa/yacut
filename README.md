# Yacut
Learning project developed on Flask. This application helps users ind URL exchange. It's really annoying that some URLs are super long. And this is a situation when Yacut could help. Application associates long URL with short one (user gets valid short URL version). Short version could be generated randomly or chosen by user. After short URL could be easily send to friends, added to presentation or published somewhere else.

Application has API with following functionality:
- /api/id/ — POST-request for short url creation
- /api/id/<short_id>/ — GET-request using short id for receiving of original url

# Authors
[IPfa](https://github.com/IPfa)
