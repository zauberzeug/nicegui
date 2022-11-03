from justpy import parse_dict, QCircularProgress, QLinearProgress


@parse_dict
class QCircularProgressExtended(QCircularProgress):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prop_list.extend(['instant-feedback'])


@parse_dict
class QLinearProgressExtended(QLinearProgress):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # add upstream missing properties
        self.prop_list.extend(['size'])
