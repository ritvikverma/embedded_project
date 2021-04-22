import re


def get_triangulated_data(vaccine_data, hkid_data):
    hkid_data = ' HONG KONG IDENTITY CARD VERMA, Ritvik HI Date of Birth 29-12-1998 CO EM Date of Issue (08-17) 28-08-17 M715467(A) Scanned with CamScanner'
    results = {'vaccination_date': vaccine_data['date'],
               'vaccine': " ".join(vaccine_data['vaccine'].split(" ")[:5]),
               'hkid_number': '',
               'name': '',
               }

    hkid_match = r'' + vaccine_data['hkid'].replace("*", '.').replace("(", "\(").replace(")", "\)")
    hkid = re.findall(hkid_match, hkid_data)
    if hkid:
        hkid = hkid[0]
        results['hkid_number'] = hkid

    name_match = r'' + vaccine_data['name'].replace('*', '.')
    name = re.findall(name_match, hkid_data)
    if name:
        name = name[0]
        results['name'] = name

    return results


def get_vaccine_data(vaccine_raw_data):
    vaccine_raw_data = vaccine_raw_data.split('|')
    vaccine_data = {'hkid': vaccine_raw_data[5],
                    'name': vaccine_raw_data[6],
                    'date': vaccine_raw_data[7],
                    'vaccine': vaccine_raw_data[8]}
    return vaccine_data


if __name__ == '__main__':
    print(get_triangulated_data({'hkid': '****467(A)', 'name': 'VERMA, R*****', 'date': '06-04-2021',
                                 'vaccine': 'Comirnaty COVID-19 mRNA Vaccine (BNT162b2) Concentrate for Dispersion for Injection'},
                                'HONG KONG IDENTITY CARD VERMA, Ritvik HI Date of Birth 29-12-1998 CO EM Date of Issue (08-17) 28-08-17 M715467(A) Scanned with CamScanner'))
