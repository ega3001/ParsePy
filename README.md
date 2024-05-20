**Parse Server Python API**

- HowTo:
    - Use:
        ```
        from parse_dal import Parse

        class MyParse(Parse):
            def get_my_class(self, class, query):
                return self.query_object(class, query)["results"]

        MyDB = MyParse({URL}, {APP}, {KEY})
        result = myDB.get_my_class({class}, {filter})
        ```
    - Install:
        Just add repo link to requirements.txt file with *git+* ahead.
        For example: `git+https://git.pancir.it/egor.bakharev/ParsePy.git`

- Useful links:
    - https://docs.parseplatform.org/rest/guide/