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
    def create_bericht(berichtinhoud, gebruiker_gebruikerid):
        sql = 'INSERT INTO bericht (berichtinhoud, gebruiker_gebruikerid) VALUES(%s,%s)'
        params = [berichtinhoud, gebruiker_gebruikerid]
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
