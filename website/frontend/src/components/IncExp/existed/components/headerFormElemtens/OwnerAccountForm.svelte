<script>
    // import { activeOnwerId, activeAccountId} from "../../../../store";
    
    export let owner_id;
    export let account_id;
    
    const createActiveOwnerAccountKey = (ownerId, accountId) => `${ownerId}_${accountId}`;
    let activeOnwerAccount = createActiveOwnerAccountKey(owner_id, account_id)
    
</script>

<input 
    type="hidden" 
    class="form-control" 
    id=owner_account_ids 
    name=owner_account_ids 
    placeholder="Właś Konto" 
    value={activeOnwerAccount}>