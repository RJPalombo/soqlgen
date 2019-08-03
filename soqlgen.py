from simple_salesforce import Salesforce, SFType
from sobject import SObject, Field
import csv

# Configuration. This is the only area you need to change.
username = ''
password = ''
security_token = ''
domain = 'login'
convert_currency = False
format_currency = False
sobject_list = ['Account', 'Contact']
file_name = 'soql.csv'

# Application name to display in Salesforce login audit
CLIENT_ID = 'SOQLGEN'

# Create Simple Salesforce instance
sf = Salesforce(username=username,
                password=password,
                security_token=security_token,
                domain=domain,
                client_id=CLIENT_ID)


def describe_sobject(sobjectname):
    sobject = SFType(sobjectname, session_id=sf.session_id,
                     sf_instance=sf.sf_instance)

    return sobject.describe()


def create_sobject(sobjectdescribe):
    sobject = SObject(
        sobjectdescribe['label'], apiname=sobjectdescribe['name'])
    for fld in sobjectdescribe['fields']:
        so_fld = Field(label=str(fld['label']),
                       apiname=str(fld['name']),
                       datatype=str(fld['type']),
                       custom=str(fld['custom']))

        sobject.add_field(so_fld)

    return sobject


def generate_soql():
    print('Creating file...')
    with open(file_name, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Object Name', 'SOQL'])

        for sobject_name in sobject_list:
            sobject = create_sobject(describe_sobject(sobject_name))
            fields = []
            for fld in sorted(sobject.fields, key=lambda f: f.custom):
                soql_fld = wrap_fld(fld)
                fields.append(soql_fld)

            soql = "SELECT %s FROM %s" % (
                ', '.join(map(str, fields)), sobject_name)
            filewriter.writerow([sobject_name, soql])
    print('File %s created!' % file_name)


def wrap_fld(fld):
    fld_name = fld.apiname
    if convert_currency and fld.datatype == 'currency':
        fld_name = 'convertCurrency(%s)' % fld_name
    if format_currency and fld.datatype == 'currency':
        fld_name = 'FORMAT(%s)' % fld_name

    return fld_name


if __name__ == '__main__':
    generate_soql()
