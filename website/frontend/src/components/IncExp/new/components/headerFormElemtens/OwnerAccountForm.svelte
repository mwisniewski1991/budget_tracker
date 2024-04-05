<script>
    import { activeOnwerId, activeAccountId} from "../../../../store";

    $: activeOnwerAccount = createActiveOwnerAccountKey($activeOnwerId, $activeAccountId)
    const createActiveOwnerAccountKey = (ownerId, accountId) => `${ownerId}_${accountId}`;
    
</script>

<input 
    type="hidden" 
    class="form-control" 
    id=owner_account_ids 
    name=owner_account_ids 
    placeholder="Właś Konto" 
    value={activeOnwerAccount}>