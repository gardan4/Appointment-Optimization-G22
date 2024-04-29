from Dash.content import app
import os

# app.server.run():
# This method directly runs the Flask development server associated with your Dash app.
# It does not include the extra setup for Dash development tools.
# Use this method when you want to run your app without the additional features provided by .run_server().
# For production deployments, it’s recommended to use gunicorn to serve your Dash app using the app.server instance12.

# app = app.server
# if __name__ == "__main__":
#     app.run(debug=True)

# app.run_server():
# This method is used to run the Dash application.
# It starts a local development server and serves your Dash app.
# When you call app.run_server(), it internally invokes app.server.run().
# Additionally, it sets up the Dash development tools for debugging and live reloading.
# Caution: Do not use this method in production deployments. It’s meant for local development only12.
#
app = app
if __name__ == "__main__":
   app.run_server(debug=True, port=8080)



