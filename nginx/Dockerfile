FROM python:3.7-slim AS server

RUN mkdir /server
WORKDIR /server

COPY ./server/requirements.txt /server/
RUN pip install -r requirements.txt

COPY ./server /server

RUN python ./manage.py collectstatic --noinput

RUN useradd -ms /bin/bash user
RUN chown -R user:user /server
RUN chmod -R 755 /server
USER user

#########################################

FROM nginx:1.13

RUN rm -v /etc/nginx/nginx.conf
COPY ./nginx/nginx.conf /etc/nginx/

RUN mkdir /nginx
COPY --from=server /server/staticfiles /nginx/static
RUN chmod 755 /nginx/static

