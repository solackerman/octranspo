from google.cloud import bigquery
from google.cloud import exceptions


class Table(object):
    dataset_id = None
    table_id = None
    schema = None

    def __init__(self):
        self.client = bigquery.Client()

        dataset_ref = self.client.dataset(self.dataset_id)
        table_ref = dataset_ref.table(self.table_id)

        try:
            self.dataset = self.client.get_dataset(dataset_ref)
        except exceptions.NotFound:
            self.dataset = self.create_dataset(self.client, dataset_ref)

        try:
            self.table = self.client.get_table(table_ref)
        except exceptions.NotFound:
            self.table = self.create_table(self.client, table_ref, self.schema)

    @staticmethod
    def create_dataset(client, dataset_ref):
        dataset = bigquery.Dataset(dataset_ref)
        return client.create_dataset(dataset)

    @staticmethod
    def create_table(client, table_ref, schema):
        table = bigquery.Table(table_ref)
        table.schema = [bigquery.SchemaField(k, v[0], **v[1])
                        for k, v in schema.items()]
        return client.create_table(table)

    def insert_rows(self, rows):
        if rows:
            return self.client.create_rows(self.table, rows)
