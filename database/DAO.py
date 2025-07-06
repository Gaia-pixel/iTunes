from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAllNodes(d):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT a.*
                        FROM album a, track t
                        WHERE a.AlbumId = t.AlbumId
                        GROUP BY a.AlbumId, a.ArtistId, a.Title
                        HAVING (SUM(t.Milliseconds)/1000/60) > %s
                                """
            cursor.execute(query, (d,))

            for row in cursor:
                result.append(Album(**row))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllArchi(d):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t.AlbumId, p.PlaylistId, p.TrackId
                        FROM track t, playlisttrack p
                        WHERE t.TrackId = p.TrackId
                        and t.AlbumId in (SELECT DISTINCT a.AlbumId
                                            FROM album a, track t
                                            WHERE a.AlbumId = t.AlbumId
                                            GROUP BY a.AlbumId, a.ArtistId, a.Title
                                            HAVING (SUM(t.Milliseconds)/1000/60) > %s)
                                    """
            cursor.execute(query, (d,))

            for row in cursor:
                result.append((row['AlbumId'], row['PlaylistId'], row['TrackId']))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllArchi2(d):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct t1.AlbumId as a1, t2.AlbumId as a2
                        FROM (SELECT t.AlbumId, p.PlaylistId, p.TrackId
                        FROM track t, playlisttrack p
                        WHERE t.TrackId = p.TrackId
                        and t.AlbumId in (SELECT DISTINCT a.AlbumId
                                            FROM album a, track t
                                            WHERE a.AlbumId = t.AlbumId
                                            GROUP BY a.AlbumId, a.ArtistId, a.Title
                                            HAVING (SUM(t.Milliseconds)/1000/60) > %s)) t1, (SELECT t.AlbumId, p.PlaylistId, p.TrackId
                                                                                                FROM track t, playlisttrack p
                                                                                                WHERE t.TrackId = p.TrackId
                                                                                                and t.AlbumId in (SELECT DISTINCT a.AlbumId
                                                                                                                    FROM album a, track t
                                                                                                                    WHERE a.AlbumId = t.AlbumId
                                                                                                                    GROUP BY a.AlbumId, a.ArtistId, a.Title
                                                                                                                    HAVING (SUM(t.Milliseconds)/1000/60) > %s)) t2
                        WHERE t1.PlaylistId = t2.PlaylistId 
                                and t1.AlbumId > t2.AlbumId
                                        """
            cursor.execute(query, (d,d))

            for row in cursor:
                result.append((row['a1'], row['a2']))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getDurata(album):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT SUM(t.Milliseconds)/1000/60 as durata
                        FROM track t
                        WHERE t.AlbumId = %s
                                        """
            cursor.execute(query, (album,))

            for row in cursor:
                result.append(row['durata'])

            cursor.close()
            cnx.close()

        return result



