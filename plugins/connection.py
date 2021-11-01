from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.connections_mdb import add_connection, all_connections, if_active, delete_connection
from info import ADMINS

@Client.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client,message):
    userid = message.reply_to_message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ Aʀᴇ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ. Usᴇ /connect {message.chat.id} Iɴ Pᴍ")
    chat_type = message.chat.type

    if chat_type == "private":
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>Eɴᴛᴇʀ Iɴ Cᴏʀʀᴇᴄᴛ Fᴏʀᴍᴀᴛ!</b>\n\n"
                "<code>/connect Gʀᴏᴜᴘ ɪᴅ</code>\n\n"
                "<i>Gᴇᴛ Yᴏᴜʀ Gʀᴏᴜᴘ Iᴅ Bʏ Aᴅᴅɪɴɢ Tʜɪs Bᴏᴛ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ Aɴᴅ Usᴇ  <code>/id</code></i>",
                quote=True
            )
            return

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
        ):
            await message.reply_text("Yᴏᴜ Sʜᴏᴜʟᴅ Bᴇ Aɴ Aᴅᴍɪɴ Iɴ Gɪᴠᴇɴ Gʀᴏᴜᴘ!", quote=True)
            return
    except Exception as e:
        print(e)
        await message.reply_text(
            "Iɴᴠᴀʟɪᴅ Gʀᴏᴜᴘ ɪᴅ!\n\nIғ Cᴏʀʀᴇᴄᴛ, Mᴀᴋᴇ Sᴜʀᴇ I'ᴍ Pʀᴇsᴇɴᴛ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ!!",
            quote=True,
        )

        return
    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == "administrator":
            ttl = await client.get_chat(group_id)
            title = ttl.title

            addcon = await add_connection(str(group_id), str(userid))
            if addcon:
                await message.reply_text(
                    f"Sᴜᴄᴇssғᴜʟʟʏ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ **{title}**\nNᴏᴡ Mᴀɴᴀɢᴇ Yᴏᴜʀ Gʀᴏᴜᴘ Fʀᴏᴍ Mʏ Pᴍ !",
                    quote=True,
                    parse_mode="md"
                )
                if chat_type in ["group", "supergroup"]:
                    await client.send_message(
                        userid,
                        f"Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ **{title}** !",
                        parse_mode="md"
                    )
            else:
                await message.reply_text(
                    "Yᴏᴜ'ʀᴇ Aʟʀᴇᴅʏ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Tʜɪs Cʜᴀᴛ!",
                    quote=True
                )
        else:
            await message.reply_text("Aᴅᴅ Mᴇ As Aɴ Aᴅᴍɪɴ Iɴ Gʀᴏᴜᴘ", quote=True)
    except Exception as e:
        print(e)
        await message.reply_text('Sᴏᴍᴇ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ! Tʀʏ Aɢᴀɪɴ Lᴀᴛᴇʀ.', quote=True)
        return


@Client.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client,message):
    userid = message.reply_to_message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Yᴏᴜ Aʀᴇ Aɴᴏɴʏᴍᴏᴜs Aᴅᴍɪɴ. Usᴇ /connect {message.chat.id} Iɴ Pᴍ"")
    chat_type = message.chat.type

    if chat_type == "private":
        await message.reply_text("Rᴜɴ /connections Tᴏ Vɪᴇᴡ Oʀ Dɪsᴄᴏɴɴᴇᴄᴛ Fʀᴏᴍ Gʀᴏᴜᴘs!", quote=True)

    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

        st = await client.get_chat_member(group_id, userid)
        if (
            st.status != "administrator"
            and st.status != "creator"
            and str(userid) not in ADMINS
        ):
            return

        delcon = await delete_connection(str(userid), str(group_id))
        if delcon:
            await message.reply_text("Sᴜᴄᴄᴇssғᴜʟʟʏ Dɪsᴄᴏɴɴᴇᴄᴛᴇᴅ Fʀᴏᴍ Tʜɪs Cʜᴀᴛ", quote=True)
        else:
            await message.reply_text("Tʜɪs Cʜᴀᴛ Isɴ'ᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Mᴇ!\nDᴏ /connect Tᴏ Cᴏɴɴᴇᴄᴛ.", quote=True)


@Client.on_message(filters.private & filters.command(["connections"]))
async def connections(client,message):
    userid = message.from_user.id

    groupids = await all_connections(str(userid))
    if groupids is None:
        await message.reply_text(
            "Tʜᴇʀᴇ Aʀᴇ Nᴏ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴs!! Cᴏɴɴᴇᴄᴛ Tᴏ Sᴏᴍᴇ Gʀᴏᴜᴘs Fɪʀsᴛ.",
            quote=True
        )
        return
    buttons = []
    for groupid in groupids:
        try:
            ttl = await client.get_chat(int(groupid))
            title = ttl.title
            active = await if_active(str(userid), str(groupid))
            act = " - ACTIVE" if active else ""
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{title}:{act}"
                    )
                ]
            )
        except:
            pass
    if buttons:
        await message.reply_text(
            "Yᴏᴜʀ Cᴏɴɴᴇᴄᴛᴇᴅ Gʀᴏᴜᴘ Dᴇᴛᴀɪʟs ;\n\n",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
