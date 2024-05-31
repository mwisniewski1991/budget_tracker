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

    results_limit = request.args.get('limit', 50)
    type_id = request.args.get('type-id', None)
    source = request.args.get('source',  None)
    created_date_from = request.args.get('created_date_from',  None)
    created_date_to = request.args.get('created_date_to',  None)
    comment = request.args.get('comment', None)
    connection = request.args.get('connection', None)

    incexp_list = (INCEXP_header
                .query
                .filter(and_(INCEXP_header.owner_id==owner_id, INCEXP_header.account_id==account_id))
                )
    
    if type_id:
        incexp_list = incexp_list.filter(INCEXP_header.type_id == type_id)


    if created_date_from:
        incexp_list = incexp_list.filter(INCEXP_header.date >= created_date_from)

    if created_date_to:
        incexp_list = incexp_list.filter(INCEXP_header.date <= created_date_to)
    
    if source:
        incexp_list = incexp_list.filter(INCEXP_header.source.ilike(f'%{source}%'))

    if created_date_from:
        incexp_list = incexp_list.filter(INCEXP_header.date >= created_date_from)

    if comment:
        incexp_list = incexp_list.filter(INCEXP_header.incexp_positions.any(INCEXP_position.comment.ilike(f"%{comment}%")))

    if connection:
        incexp_list = incexp_list.filter(INCEXP_header.incexp_positions.any(INCEXP_position.connection.ilike(f"%{connection}%")))


    incexp_list = (incexp_list
                    .order_by(INCEXP_header.date.desc(), INCEXP_header.id)
                    .limit(results_limit)
                   ).all()
    
    return render_template("incexp/home.html.jinja", incexp_list=incexp_list)

@incexp.route('/owners-accounts', methods=['GET'])
def get_owners_accounts():
    owners = Owners.query.order_by(Owners.id).all()
    return render_template("incexp/owners_accounts_dropdown.html.jinja", owners=owners)
