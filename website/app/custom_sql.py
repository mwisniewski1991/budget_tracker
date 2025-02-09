insert_types = '''
    INSERT INTO public.type_dict (id, name_eng, name_pl)
    VALUES 
        ('1', 'Expense', 'Wydatek'),
        ('2', 'Income', 'Dochód')
    ON CONFLICT DO NOTHING;
'''