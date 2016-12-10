from wikidataviz.models.jobs import DeferredResource


class JobResource(DeferredResource):
    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('id', type=str, required=True)

    def get(self):
        args = self.get_parser.parse_args()
        return self.check_job(args['id'])
