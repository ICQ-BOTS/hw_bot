box.cfg{
    listen=3301
}

box.schema.user.grant('guest', 'read,write,execute', 'universe', nil, {if_not_exists=true})
box.once("hw", function()
    box.schema.space.create('user', {
        if_not_exists = true,
        format={
            {name = 'user_id', type = 'string'},
            {name = 'update', type = 'boolean'},
            {name = 'old_mes', type = 'map'},
            {name = 'schedule', type = 'map'},
            {name = 'homework', type = 'map'}
        }
    })
    box.space.user:create_index('id', {
        type = 'hash',
        parts = {'user_id'},
        if_not_exists = true,
        unique = true
    })
end
)


