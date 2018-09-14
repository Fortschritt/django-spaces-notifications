$(function () {
	var memForm = '#id_form-0-notify_these_members_0';
	var roleForm = '#id_form-0-notify_by_role_0';
	console.log($(roleForm));

	var toggleTeamMembers = function(ev) {
		var selector = memForm + ' div.custom-checkbox[data-is-team="True"] input'
		var val = $(ev.target).prop('checked')
		$(selector).prop('checked', val);
	}

	var toggleAdminMembers = function(ev) {
        var selector = memForm + ' div.custom-checkbox[data-is-admin="True"] input'
        var val = $(ev.target).prop('checked')
        $(selector).prop('checked', val);
    }

	var toggleAllMembers = function(ev) {
        var selector = memForm + ' div.custom-checkbox input'
        var val = $(ev.target).prop('checked')
        $(selector).prop('checked', val);
    }

	$(roleForm + ' input[value="team"]').on('click', toggleTeamMembers);
	$(roleForm + ' input[value="admins"]').on('click', toggleAdminMembers);
	$(roleForm + ' input[value="all"]').on('click', toggleAllMembers);
});