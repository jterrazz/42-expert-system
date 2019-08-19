# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jterrazz <jterrazz@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2019/04/23 18:00:29 by jterrazz          #+#    #+#              #
#    Updated: 2019/07/25 10:57:25 by jterrazz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = expert_system

.PHONY: expert_system all tests

# **************************************************************************** #
# COMMANDS  		    													   #
# **************************************************************************** #

all: $(NAME)

$(NAME):
    virtualenv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    brew install graphviz

test: #
    python3 -m pytest -v
