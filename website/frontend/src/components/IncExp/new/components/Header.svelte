<script>
    import OwnerAccountForm from "./headerFormElemtens/OwnerAccountForm.svelte";
    import SourcesForm from "./headerFormElemtens/SourcesForm.svelte";
    import TypeForm from "./headerFormElemtens/TypeForm.svelte";
    import DateForm from "./headerFormElemtens/DateForm.svelte";
    import AmountForm from "./headerFormElemtens/AmountForm.svelte";

    export let currentTypeId;
</script>


<div class="col"><OwnerAccountForm/></div>
<div class="row">
    <div class="col"><TypeForm bind:currentTypeId/></div>
    <div class="col-4"><DateForm/></div>
    <div class="col-4"><SourcesForm/></div>
    <div class="col"><AmountForm/></div>
</div>