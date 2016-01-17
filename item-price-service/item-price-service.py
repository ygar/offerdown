from flask import Flask, request, abort, jsonify
import psycopg2
import redis
import ast
import settings

app = Flask(__name__)


select_list_price_query = '''
SELECT list_price
FROM "itemPrices_itemsale"
WHERE title = %s 
'''

cache = redis.Redis.from_url(settings.CACHE_URL)


# Filters item prices from database based on item title(required) and city(optional)
def filter_item_prices(item, city=None):
	query = select_list_price_query	
	query_args = [item]
	if city is not None:
		query += ("AND city = %s")
		query_args.append(city)

	conn = psycopg2.connect(settings.DB_CONNECTION_STRING)
	cursor = conn.cursor()
	cursor.execute(query, query_args)
	query_result = cursor.fetchall()
	cursor.close()
	conn.close()	
	items = [i[0] for i in query_result if i is not None]
	return items


# Calculates the mode for a list of positive integers. If there's a tie, returns the largest value
def calculate_mode(items):
	counts = {}
	for item in items:
		if item not in counts:
			counts[item] = 1
		else:
			counts[item] += 1
	highest_item_count = 0
	mode = 0
	for item in items:
		count = counts[item]
		if count > highest_item_count:
			highest_item_count = count
			mode = item
		elif count == highest_item_count and item > mode:
			mode = item
	return mode, highest_item_count


@app.route("/item-price-service/", methods = ['GET'])
def main():
	item = request.args.get('item')
	if item is None:
		result = {"status": 404, "content":{"message": "Not Found"}}
	city = request.args.get('city')

	cache_key = item + "_" + str(city)
	cached_result = cache.get(cache_key)
	if cached_result is not None:
		result = ast.literal_eval(cached_result)
	else:
		try:
			items = filter_item_prices(item, city)
			price_suggestion, item_count = calculate_mode(items)
			if city is None:
				city = "Not specified"
			result = {"status": 200, "content":{"item": item, "item_count": item_count, "price_suggestion": price_suggestion, "city": city}}
			cache.setex(cache_key, result, settings.CACHE_TIMEOUT_TIME)
		except Exception as e:
			result = {"status": 500, "content":{"message": "Internal Server Error"}}

	return jsonify(result)


if __name__ == "__main__":
    app.run(host=settings.LOCALHOST, port=5000, debug=True)
