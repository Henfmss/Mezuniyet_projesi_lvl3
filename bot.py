import discord 
from discord.ext import commands
from config import TOKEN, gemini_api_key
import logic
from logic import select_data
from google import genai
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
client = genai.Client(api_key=gemini_api_key)


@bot.event
async def on_ready():
    print(f"{bot.user.name} başarıyla çalıştırıldı ve hazır!")


@bot.command()
async def meslekler(ctx):
    meslekler_bilgi = select_data()
    
    if not meslekler_bilgi:
        await ctx.send("Veritabanında henüz gösterilecek meslek bulunmuyor.")
        return

    embed = discord.Embed(
        title="🎲 Rastgele 5 Meslek Önerisi",
        description="Aşağıda veritabanından rastgele seçilen meslekleri bulabilirsiniz:",
        color=discord.Color.blue()
    )

    for meslek, aciklama, video in meslekler_bilgi:
        embed.add_field(
            name=f"💼 {meslek}",
            value= f"{aciklama}, {video}" if aciklama else "Açıklama bulunmuyor.",
            inline=False
        )

    embed.set_footer(text=f"İsteyen: {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)


@bot.command()
async def ai(ctx, *, soru):
    # Kullanıcıya yanıt hazırlanırken bildirim gönder
    async with ctx.typing():
        prompt = f"{soru} (Lütfen cevabı 1500 karakteri geçmeyecek şekilde özetle.)"
        
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )
        
        cevap = interaction.output_text[:1900]

        # AI yanıtı için Embed yapısı
        embed = discord.Embed(
            title="🤖 Gemini AI Yanıtı",
            description=cevap,
            color=discord.Color.purple()
        )
        embed.add_field(name="❓ Sorulan Soru", value=soru, inline=False)
        embed.set_footer(text=f"Soran: {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)

import asyncio

@bot.command()
async def mulakat(ctx, *, meslek: str):
    async with ctx.typing():
        # 1. AI'dan mülakat sorusu iste
        prompt_soru = f"{meslek} mesleği için iş mülakatında sorulabilecek gerçekçi ve teknik/davranışsal 1 adet mülakat sorusu sor."
        
        response_soru = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt_soru
        )
        soru_metni = response_soru.text

        # Soruyu Discord'a gönder
        embed = discord.Embed(
            title=f"🎙️ {meslek.capitalize()} Mülakat Soru Simülasyonu",
            description=f"**Mülakatçının Sorusu:**\n{soru_metni}\n\n*Lütfen yanıtınızı 150 saniye içinde bu kanala yazın.*",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    # 2. Kullanıcının vereceği cevabı kontrol eden fonksiyon
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        # Kullanıcının yanıtını  saniye boyunca bekle
        user_response = await bot.wait_for('message', timeout=150.0, check=check)
    
    except asyncio.TimeoutError:
        await ctx.send(f"⏱️ {ctx.author.mention}, yanıt verme süreniz doldu. Mülakat sonlandırıldı.")
        return

    # 3. Kullanıcının verdiği cevabı AI ile değerlendir
    async with ctx.typing():
        prompt_degerlendirme = (
            f"Mülakat Sorusu: {soru_metni}\n"
            f"Adayın Cevabı: {user_response.content}\n\n"
            f"Lütfen adayın verdiği cevabı değerlendir. Cevabın güçlü ve zayıf yönlerini belirt, "
            f"10 üzerinden bir puan ver ve nasıl daha iyi cevap verebileceğine dair kısa bir tavsiye yaz."
        )

        response_eval = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt_degerlendirme
        )

        embed_eval = discord.Embed(
            title="📊 Mülakat Değerlendirme Sonucu",
            description=response_eval.text[:1900],
            color=discord.Color.green()
        )
        embed_eval.set_footer(text=f"Aday: {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=embed_eval)

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="ℹ️ Bot Bilgilendirme ve Komut Rehberi",
        description="Bu bot, veritabanı sorguları ve yapay zeka entegrasyonu ile çeşitli işlevler sunar.",
        color=discord.Color.green()
    )

    embed.add_field(
        name="📌 !meslekler",
        value="Veritabanından (`meslekler.db`) rastgele 5 adet meslek ve açıklamasını getirir.",
        inline=False
    )
    embed.add_field(
        name="📌 !ai <sorunuz>",
        value="Google Gemini AI modelini kullanarak sorduğunuz sorulara akıllı yanıtlar üretir.",
        inline=False
    )
    embed.add_field(
        name="📌 !info",
        value="Botun tüm komutlarını ve ne işe yaradıklarını açıklayan bu menüyü görüntüler.",
        inline=False
    )
    embed.add_field(
        name="📌 !meslek_ara <meslek>",
        value="Yazdığınız mesleğin açıklamasını ve onun hakkında bilgi veren bazı linkler verir.",
        inline=False
    )

    embed.set_footer(text=f"İsteyen: {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def meslek_ara(ctx,*,meslek):
    prompt = f"{meslek}Mesleğin hakkında bilgilendirici güvenilir bir web sitesi linki ver"
    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt
    )
        
    cevap = interaction.output_text[:1900]


    embed = discord.Embed(
        title="🤖 Gemini AI Yanıtı",
        description=cevap,
        color=discord.Color.purple()
    )
    embed.set_footer(text=f"Soran: {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed)


@bot.command()
async def kariyer_testi(ctx):
    sorular = [
        "1/4: Günlük hayatta sorun çözerken daha çok **analitik/teknik** yolları mı yoksa **yaratıcı/sanatsal** yolları mı tercih edersin?",
        "2/4: İnsanlarla sürekli iletişimde olduğun bir işte mi yoksa kendi başına/ekran başında çalıştığın bir işte mi daha verimli olursun?",
        "3/4: En çok ilgini çeken alan hangisi? (Örn: Yazılım, Tıp, Tasarım, Ticaret, Eğitim, Hukuk vb.)",
        "4/4: Çalışma ortamı hayalin nedir? (Masa başı/Ofis, Sahada/Açık hava, Evden/Uzaktan)"
    ]

    cevaplar = []

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send(f"🎯 **{ctx.author.mention}, Kariyer Testine Hoş Geldin!**\nSana 4 adet soru soracağım. Lütfen her soruyu yanıtla. İlk soru geliyor:")

    for soru in sorular:
        embed_soru = discord.Embed(
            title="❓ Kariyer Testi",
            description=soru,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed_soru)

        try:
            msg = await bot.wait_for('message', timeout=90.0, check=check)
            cevaplar.append(msg.content)
        except asyncio.TimeoutError:
            await ctx.send(f"⏱️ {ctx.author.mention}, yanıt verme süreniz (90 sn) doldu. Test iptal edildi.")
            return

    async with ctx.typing():
        prompt = (
            f"Bir kullanıcıya kariyer testi yapıldı. Verilen yanıtlar şunlardır:\n"
            f"1. Problem çözme tarzı: {cevaplar[0]}\n"
            f"2. Çalışma şekli/İletişim: {cevaplar[1]}\n"
            f"3. İlgi alanı: {cevaplar[2]}\n"
            f"4. Ortam tercihi: {cevaplar[3]}\n\n"
            f"Bu yanıtlara göre kullanıcıya en uygun 3 mesleği belirle. "
            f"Her meslek için neden uygun olduğunu kısa ve net bir şekilde açıkla."
        )

        # Projenizdeki mevcut API çağrı yapısı:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )
        
        cevap = interaction.output_text[:1900]

        embed_sonuc = discord.Embed(
            title="✨ Sana En Uygun Kariyer & Meslek Önerileri",
            description=cevap,
            color=discord.Color.gold()
        )
        embed_sonuc.set_footer(text=f"Testi Tamamlayan: {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=embed_sonuc)


bot.run(TOKEN)