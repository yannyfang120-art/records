import db

def add_item(album, artist, review, review_points, user_id):
	sql = """ INSERT INTO items (album, artist, review, review_points, user_id)
				VALUES (?, ?, ?, ?. ?)"""
	db.execute(sql, [album, artist, review, review_points, user_id])