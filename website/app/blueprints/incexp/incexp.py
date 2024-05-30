from flask import Blueprint, render_template, request, send_from_directory, redirect, jsonify
from sqlalchemy import text, and_, select, func, case, alias
from ... import db
from ...models import Owners, INCEXP_header, INCEXP_position, Type, Accounts
import logging

DEFAULT_OWNER_ACCOUNT_IDS = '1_05'

incexp = Blueprint (
                    'incexp', 
                    __name__,
                    template_folder="templates",
                    static_folder="static")

@incexp.route('/', methods=['GET'])
def get_incexp():
    owner_account_ids = request.args.get('owner-account-ids', DEFAULT_OWNER_ACCOUNT_IDS)
    owner_id, account_id = owner_account_ids.split('_')

    incexp_list = (INCEXP_header
                .query
                .filter_by(owner_id=owner_id, account_id=account_id)
                .order_by(INCEXP_header.date.desc(), INCEXP_header.id)
                .limit(5)
            ).all()


    # incexp_list = (db.session.query(INCEXP_header, INCEXP_position, Type, Owners, Accounts)
    #             .join(INCEXP_position, INCEXP_header.id == INCEXP_position.header_id)
    #             .join(Type, INCEXP_header.type_id == Type.id)
    #             .join(Owners, INCEXP_header.owner_id == Owners.id)
    #             .join(Accounts, INCEXP_header.account_id == Accounts.id)
    #             .filter(and_(
    #                             INCEXP_header.owner_id == owner_id, 
    #                             INCEXP_header.account_id == account_id,
    #                         ))
    #             .order_by(INCEXP_header.date.desc(), INCEXP_header.id)
    #             .limit(5)
    #             ).all()
    

    # logging.warning(incexp_list[0].INCEXP_header)
    return render_template("incexp/home.html.jinja", incexp_list=incexp_list)

@incexp.route('/owners-accounts', methods=['GET'])
def get_owners_accounts():
    owners = Owners.query.order_by(Owners.id).all()
    return render_template("incexp/owners_accounts_dropdown.html.jinja", owners=owners)
