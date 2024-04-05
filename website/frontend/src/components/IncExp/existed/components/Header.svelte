<script>
    import HeaderIdForm from "./headerFormElemtens/HeaderIdForm.svelte";
    import OwnerAccountForm from "./headerFormElemtens/OwnerAccountForm.svelte";
    import SourcesForm from "./headerFormElemtens/SourcesForm.svelte";
    import TypeForm from "./headerFormElemtens/TypeForm.svelte";
    import DateForm from "./headerFormElemtens/DateForm.svelte";
    import AmountForm from "./headerFormElemtens/AmountForm.svelte";

    export let currentTypeId;
    export let isModifyMode;
    export let IncExp;

</script>


<div class="col">
    <OwnerAccountForm owner_id={IncExp['owner_id']} account_id={IncExp['account_id']}/>
    <HeaderIdForm headerId={IncExp['header_id']}/>
</div>

<div class="row">
    <div class="col"><TypeForm bind:currentTypeId isModifyMode={isModifyMode} type_id={IncExp['type_id']} type_name={IncExp['type_name']} /></div>

    <div class="col-4"><DateForm isModifyMode={isModifyMode} header_date={IncExp['header_date']}/></div>

    <div class="col-4"><SourcesForm isModifyMode={isModifyMode} source={IncExp['source']}/></div>

    <div class="col"><AmountForm total_amount={IncExp['total_amount']}/></div>
</div>
