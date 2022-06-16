from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_device():
        sql = "SELECT * from device"
        return Database.get_rows(sql)

    @staticmethod
    def read_device_by_id(id):
        sql = "SELECT * from device WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def create_historiek(Device_deviceid, actie_actieid, datum, waarde, commentaar):
        sql = 'INSERT INTO historiek (Device_deviceid,actie_actieid,bericht_berichtid,datum,waarde,commentaar) VALUES(%s,%s,NULL,%s,%s,%s)'
        params = [Device_deviceid, actie_actieid, datum, waarde, commentaar]
        result = Database.execute_sql(sql, params)
        return result

    @staticmethod
    def create_historiek_bij_bericht(actie_actieid, bericht_berichtid, datum, commentaar):
        sql = 'INSERT INTO historiek (Device_deviceid,actie_actieid,bericht_berichtid,datum,waarde,commentaar) VALUES(NULL,%s,%s,%s,NULL,%s)'
        params = [actie_actieid, bericht_berichtid, datum, commentaar]
        result = Database.execute_sql(sql, params)
        return result

    @staticmethod
    def create_bericht(berichtinhoud, gebruiker_gebruikerid, ontvanger):
        sql = 'INSERT INTO bericht (berichtinhoud, gebruiker_gebruikerid,ontvanger) VALUES(%s,%s,%s)'
        params = [berichtinhoud, gebruiker_gebruikerid, ontvanger]
        result = Database.execute_sql(sql, params)
        return result

    @staticmethod
    def create_user(naam):
        sql = 'INSERT INTO bericht (naam) VALUES(%s)'
        params = [naam]
        result = Database.execute_sql(sql, params)
        return result

    @staticmethod
    def read_id_laatste_bericht():
        sql = "SELECT max(berichtid) from bericht"
        return Database.get_rows(sql)

    @staticmethod
    def create_user(naam):
        sql = 'INSERT INTO gebruiker (naam) VALUES(%s)'
        params = [naam]
        result = Database.execute_sql(sql, params)
        return result

    @staticmethod
    def read_user_by_naam(naam):
        sql = "SELECT * FROM gebruiker WHERE naam = %s"
        params = [naam]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_historiek_temp():
        sql = "select round(avg(waarde),2) as waarde , concat(DAY(datum),' ',MONTHNAME(datum)) as datum from historiek WHERE actie_actieid = 1 group by day(datum)"
        return Database.get_rows(sql)

    @staticmethod
    def read_berichten_by_id(id, ontvanger, id2, ontvanger2):
        sql = "SELECT * FROM bericht WHERE gebruiker_gebruikerid in (%s,%s) and ontvanger in (%s,%s)"
        params = [id, ontvanger, id2, ontvanger2]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_gebruikers_by_id(id):
        sql = "SELECT * FROM gebruiker WHERE gebruikerid = %s"
        params = [id]
        return Database.get_rows(sql, params)

    @staticmethod
    def read_berichtdatum_historiek(id, ontvanger, id2, ontvanger2):
        sql = "SELECT * FROM bericht c JOIN historiek h ON c.berichtid = h.bericht_berichtid JOIN gebruiker g ON c.gebruiker_gebruikerid = gebruikerid WHERE c.gebruiker_gebruikerid in(%s,%s) and c.ontvanger in(%s,%s) ORDER BY c.berichtid"
        params = [id, ontvanger, id2, ontvanger2]
        return Database.get_rows(sql, params)

    def read_historiek_temp_dag():
        sql = "select * from historiek where datum between date_sub(now(),INTERVAL 1 DAY) and now() and actie_actieid = 1"
        return Database.get_rows(sql)

    def read_historiek_temp_week():
        sql = "select round(avg(waarde),2) as waarde , concat(DAY(datum),' ',MONTHNAME(datum)) as datum from historiek where datum between date_sub(now(),INTERVAL 1 WEEK) and now() and actie_actieid = 1 group by day(datum)"
        return Database.get_rows(sql)

    def read_historiek_berichten_week():
        sql = "select count(datum) as 'aantal',concat(DAY(datum),' ',MONTHNAME(datum)) as 'datum' from historiek where datum between date_sub(now(),INTERVAL 1 WEEK) and now() and actie_actieid = 10 group by day(datum)"
        return Database.get_rows(sql)

    def read_historiek_berichten():
        sql = "select count(datum) as 'aantal', concat(DAY(datum),' ',MONTHNAME(datum)) as 'datum' from historiek WHERE actie_actieid = 10 group by day(datum)"
        return Database.get_rows(sql)
