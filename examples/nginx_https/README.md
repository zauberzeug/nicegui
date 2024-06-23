# Serving an App with HTTPS Encryption behind a Reverse Proxy (NGINX)

This example shows how to serve NiceGUI with HTTPS encryption behind NGINX.
For running the app under a subpath, have a look at https://github.com/zauberzeug/nicegui/blob/main/examples/nginx_subpath.

## Try Out

1. Create the `certs/` directory:

   ```bash
   mkdir certs
   ```

2. Generate and self-sign an SSL certificate for "localhost":

   ```bash
   openssl req -x509 -out certs/localhost.crt -keyout certs/localhost.key -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost' -extensions EXT -config <( printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
   ```

3. Run the containerized app:

   ```bash
   docker compose up
   ```

4. Try to access http://localhost (without the "s").
   You will be automatically redirected to the HTTPS version.

5. Depending on your browser, you should typically receive a warning that the certificate authority is invalid.
   This is perfectly normal as we issued and self-signed a simple certificate for demo use locally.
   So proceed anyway, e.g. on Chrome, click on "Advanced" > "Proceed to localhost (unsafe)".

6. Note the "Hello World" message from the app accessed with encrypted connection.

## Deploy in production in your self-hosted NGINX

- For production, you will need your own domain and a proper SSL certificate issued by a recognized Certificate Authority (CA).
  You can consider the free CA [Let's Encrypt](https://letsencrypt.org/) provided by the Internal Security Research Group, and use their [Certbox](https://certbot.eff.org/instructions) tool to generate the certificates for your own domain.

- If you already have an NGINX server running and want to add your NiceGUI app,
  you can reuse a stripped-down version of the nginx.conf file,
  [nginx_site.conf](https://github.com/zauberzeug/nicegui/blob/main/example/nginx_https/nginx_site.conf).

```bash
sudo cp nginx_site.conf /etc/nginx/sites-available/my_nicegui_app.conf
sudo nano /etc/nginx/sites-available/my_nicegui_app.conf # customize your domain, certificates, port number, etc.
sudo ln -s /etc/nginx/sites-available/mynicegui_app.conf /etc/nginx/sites-enabled
sudo systemctl reload nginx
```
