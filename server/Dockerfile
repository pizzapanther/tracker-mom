FROM bitnami/minideb:bookworm

ARG userid
ARG groupid

RUN install_packages python3-full curl wget unzip pipx

WORKDIR /tmp
RUN wget -O scripts.zip https://gist.github.com/pizzapanther/e341fd980d8469724465018db657d529/archive/9feb4b9a6683b8534f9d906bdbafc24747740667.zip
RUN unzip -j scripts.zip
RUN chmod 777 *.bsh
RUN ls -lha
RUN /tmp/group_init.bsh $groupid
RUN /tmp/user_init.bsh $userid $groupid

RUN mkdir -p /app
RUN chown -R $userid:$groupid /app
WORKDIR /app

USER $userid

ENV UV_LINK_MODE=copy
RUN /tmp/dx_init.bsh
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN pipx ensurepath && pipx install pdm && pipx inject pdm pdm-django
