<script>
    import { activeOnwerId, activeAccountId} from "../../store.js";
    import DeleteHeaderButton from "./components/buttons/DeleteHeaderButton.svelte";
    import ModifyHeaderButton from "./components/buttons/ModifyHeaderButton.svelte";
    import PostHeaderButton from "./components/buttons/PostHeaderButton.svelte";
    import Header from "./components/Header.svelte";
    import Positions from "./components/Positions.svelte";
    
    export let IncExp;
    
    let method_route = `/api/v1/owners/${$activeOnwerId}/accounts/${$activeAccountId}/incexp/${IncExp['header_id']}`
    let currentTypeId;
    let isModifyMode;
</script>

<div class="container container-border">
    
    <form action={method_route} method="post">
            <div>
                <DeleteHeaderButton headerIDtoDelete={IncExp['header_id']}/>
                <ModifyHeaderButton bind:isModifyMode/>
                <PostHeaderButton isModifyMode={isModifyMode}/>
            </div>
            
            <Header 
                bind:currentTypeId
                isModifyMode={isModifyMode}
                IncExp={IncExp}
                />

            
            {#each IncExp['positions'] as position }
                <Positions 
                    isModifyMode={isModifyMode}
                    currentTypeId={currentTypeId}
                    PositionData={position} 
                    typeId = {IncExp['type_id']}
                    />
            {/each}

        </form>

</div>

<style>
    .container-border{
        border: 1px solid white;
         border-radius: 10px;
        padding: 5px 5px;
        margin-bottom: 20px;
    }
</style>