import discord
import sqlite3

TOKEN = 'トークンを設定'
INSERT_SQL = 'INSERT INTO todo(value, user, delflg) values(?,?,?);'
DEL_SQL = 'UPDATE todo set delflg = 1 where id = ?;'
SELECT_SQL = 'SELECT id, value, user, created_datetime from todo where delflg=0;'
DBNAME = 'sqlite.db'
conn = sqlite3.connect(DBNAME)
conn.row_factory = sqlite3.Row

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):

    if message.author.bot:
#        print('botは無視')
        return
    else:
        # メンションがついた場合のみ
        if client.user in message.mentions:
            parameters = message.content.split()
            command = parameters[1]

            print(command)

            # /addの場合
            if command == '/add':
                # パラメータの個数チェック
                if len(parameters) < 3:
                    await message.channel.send('/add やりたいこと')
                    return

                # コネクション取得
                cur = conn.cursor()

                # やりたいこと結合
                yaritaiAry = parameters[2:]
                yaritai = ' '. join(yaritaiAry)

                # データ登録
                inserts=[
                        (yaritai,message.author.name,0)
                        ]

                cur.executemany(INSERT_SQL,inserts)
                conn.commit()

                listValue = getList()

                await message.channel.send('登録しました！\n'+listValue)

                return

            # /delの場合
            if command == '/del':
                if len(parameters) != 3:
                    await message.channel.send('/del ID')
                    return
            
                # カーソル取得
                cur = conn.cursor()

                # データ登録
                key=[
                    (int(parameters[2]),)
                    ]

                cur.executemany(DEL_SQL,key)
                conn.commit()

                listValue = getList()

                await message.channel.send('削除しました！\n' + listValue)

                return
            
            # list
            if command == '/list':
                
                ## カーソル取得
                #cur = conn.cursor()

                #cur.execute(SELECT_SQL)
                #listValue = ''
                #for row in cur:
                #    listValue = listValue + str(row['id']) + ' ' + row['user'] + ' ' + row['value'] + '\n'

                listValue = getList()

                await message.channel.send(listValue) 

                return

            await message.channel.send('▼使い方\n/add やりたいこと\n/del id\n/list\n')
            return

def getList():
    # カーソル取得
    cur = conn.cursor()

    cur.execute(SELECT_SQL)
    listValue = ''
    for row in cur:
        listValue = listValue + str(row['id']) + ' ' + row['user'] + ' ' + row['value'] + '\n'

    return listValue

client.run(TOKEN)
