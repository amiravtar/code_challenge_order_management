# Dockerfile
FROM postgres:17.4

# Install the locale for Persian (fa_IR.UTF-8)
RUN localedef -i fa_IR -c -f UTF-8 -A /usr/share/locale/locale.alias fa_IR.UTF-8

# Set the environment variable for the default language
ENV LANG=fa_IR.utf8
