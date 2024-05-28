from flask import Blueprint, render_template, request, send_from_directory, redirect, jsonify
from sqlalchemy import text, and_, select, func, case, alias
from .. import db
from ..models import INCEXP_header, INCEXP_position, Owners, Accounts

accounts_results = Blueprint (
                    'accounts_results', 
                    __name__,
                    template_folder="templates",
                    static_folder="static")

@accounts_results.route("/", methods=['GET'])
def accounts_results_home():
    results = (db.session.query(
                        INCEXP_header.owner_id, 
                        INCEXP_header.account_id, 
                        Owners.name_pl,
                        Accounts.name_pl,
                        func.sum(case(
                                (INCEXP_header.type_id == '1', INCEXP_position.amount_absolute * -1),
                                (INCEXP_header.type_id == '2', INCEXP_position.amount_absolute),
                            )),
                        func.max(INCEXP_position.updated_at_cet)
                        )
                    .join(INCEXP_position, INCEXP_header.id == INCEXP_position.header_id)
                    .join(Owners, INCEXP_header.owner_id == Owners.id)
                    .join(Accounts, INCEXP_header.account_id == Accounts.id)
                    .group_by(INCEXP_header.owner_id, INCEXP_header.account_id, Owners.name_pl, Accounts.name_pl)
                    .order_by(INCEXP_header.owner_id, INCEXP_header.account_id)
                ).all()

    unique_owners_list = sorted({ (owner_row[0], owner_row[2] ) for owner_row in results }) 

    owners = [
        {
            'id':owner[0],
            'name' : owner[1],
            'accounts' : [
                {
                    "id":  str(account[1]).strip(),
                    "name":  str(account[3]).strip(),
                    "amount_sum": account[4],
                    "last_update": str(account[5].strftime('%Y-%m-%d'))
                } for account in list(filter(lambda x: x[0] ==  owner[0], results))
            ]
        } for owner in unique_owners_list
    ]

    return render_template ('accounts_results/home.html.j2', owners=owners)
