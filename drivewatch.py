from fabric import Connection
import texttable


ssh_key ='/path/to/key/file'

### Setup server connections
# trinity-0
trinity_0 = Connection('trinity-0.home.darkmage.org', connect_kwargs={
    'key_filename': ssh_key 
})
trinity_0.prettyname = 'trinity-0'
trinity_0.arrays = ['0']
trinity_0.array_size = 24

# backup-server
backup_server = Connection('backup-server.home.darkmage.org', connect_kwargs={
    'key_filename': ssh_key
})
backup_server.prettyname = 'backup-server'
backup_server.arrays = ['0', '10', '1']
backup_server.array_size = 12


serverlist = {
    'trinity_0': trinity_0,
    'backup_server': backup_server
}


### The land of functions

##
# external functions - i.e. functions that can be called from outside this module
##

async def trinity_table():
    trinity0table = texttable.Texttable()
    trinity0table.set_cols_align(["c", "c", "c", "c"])
    trinity0table.add_rows(await twentyfourdrive(trinity_0), header=False)
    a = '```\n'
    a = a + trinity0table.draw()
    a = a + '\n```'
    return a


async def backup_table():
    backuptable = texttable.Texttable()
    backuptable.set_cols_align(["c", "c", "c"])
    backuptable.add_rows(await twelvedrive(backup_server), header=False)
    a = '```\n'
    a = a + backuptable.draw()
    a = a + '\n```'
    return a


async def reallocated_sectors(server):
    g = ''
    for h in serverlist.get(server).arrays:
        for i in range(serverlist.get(server).array_size):
            rac = await command_formatted(serverlist.get(server), f'tw-cli /c{h}/p{i} show rasect')
            if rac != '0':
                g = g + f'{serverlist.get(server).prettyname}/c{h}/p{i}: {rac}'
                g = g + '\n'
    return g


async def all_status():
    g = ''
    for i in trinity_0, backup_server:
        g = g + await array_status(i)
        g = g + '\n'
    return g


async def drive_status(server):
    g = f'{serverlist.get(server)}:'
    g = g + '\n'
    for h in serverlist.get(server).arrays:
        for i in range(serverlist.get(server).array_size):
            ds = await command_formatted(serverlist.get(server), f'tw-cli /c{h}/p{i} show status')
            if ds != 'OK':
                g = g + f'{serverlist.get(server).prettyname}/c{h}/p{i}: {ds}'
                g = g + '\n'
    return g


###
# internal functions - the gum and string holding this whole show together
###


async def run_command(server, command):
    a = server.sudo(command, hide=True)
    return a.stdout


async def command_formatted(server, command):
    a = await run_command(server, command)
    a = a.split(" = ")[1]
    return a.strip()


async def twentyfourdrive(server):
    loa = [
        [5, 11, 17, 23],
        [4, 10, 16, 22],
        [3, 9, 15, 21],
        [2, 8, 14, 20],
        [1, 7, 13, 19],
        [0, 6, 12, 18]
    ]
    for b in range(len(loa)):
        for c in range(len(loa[0])):
            t = await command_formatted(server, f'tw-cli /c0/p{loa[b][c]} show temperature')
            r = await command_formatted(server, f'tw-cli /c0/p{loa[b][c]} show rasect')
            d = f'{loa[b][c]}, {t}, {r}'
            loa[b][c] = d
    return loa


async def twelvedrive(server):
    toa = [
        ['/c0/p11', '/c10/p11', '/c1/p11'],
        ['/c0/p10', '/c10/p10', '/c1/p10'],
        ['/c0/p9', '/c10/p9', '/c1/p9'],
        ['/c0/p8', '/c10/p8', '/c1/p8'],
        ['/c0/p7', '/c10/p7', '/c1/p7'],
        ['/c0/p6', '/c10/p6', '/c1/p6'],
        ['/c0/p5', '/c10/p5', '/c1/p5'],
        ['/c0/p4', '/c10/p4', '/c1/p4'],
        ['/c0/p3', '/c10/p3', '/c1/p3'],
        ['/c0/p2', '/c10/p2', '/c1/p2'],
        ['/c0/p1', '/c10/p1', '/c1/p1'],
        ['/c0/p0', '/c10/p0', '/c1/p0'],
    ]
    for b in range(len(toa)):
        for c in range(len(toa[0])):
            t = await command_formatted(server, f'tw-cli {toa[b][c]} show temperature')
            r = await command_formatted(server, f'tw-cli {toa[b][c]} show rasect')
            d = f'{toa[b][c]}, {t}, {r}'
            toa[b][c] = d
    return toa


async def array_status(server):
    g = ''
    for h in server.arrays:
        cs = await command_formatted(server, f'tw-cli /c{h}/u0 show status')
        if cs != 'OK':
            if cs == 'REBUILDING' or cs == 'REBUILD-VERIFY' or cs == 'REBUILD-INIT':
                ecs = await command_formatted(server, f'tw-cli /c{h}/u0 show rebuildstatus')
            elif cs == 'VERIFYING':
                ecs = await command_formatted(server, f'tw-cli /c{h}/u0 show verifystatus')
            elif cs == 'INITIALIZING':
                ecs = await command_formatted(server, f'tw-cli /c{h}/u0 show initializestatus')
            else:
                ecs = '???'
            g = g + f'{server.prettyname}/{h} state {cs} {ecs}'
            g = g + '\n'
        else:
            pass
    return g
